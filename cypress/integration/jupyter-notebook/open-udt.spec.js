context("Open UDT Image Classification Dataset", () => {
  it("log into jupyter notebook and create new notebook", () => {
    cy.visit("http://localhost:8888")
    cy.contains("Log in").click()
    cy.contains("New").click()

    cy.wait(500)

    const win = cy.window().then(async (win) => {
      console.log({ Jupyter: win.Jupyter })

      const {
        name,
      } = await win.Jupyter.new_notebook_widget.contents.new_untitled("", {
        type: "notebook",
      })

      cy.visit(`http://localhost:8888/notebooks/${name}`)
    })
  })

  it("should be able to import udt and open a dataset", () => {
    const runCell = (andInsert = true) => {
      cy.wait(100)
      cy.get(".dropdown-toggle").contains("Cell").click()
      if (andInsert) {
        cy.contains("Run Cells and Insert Below").click()
      } else {
        cy.contains("Run Cells").click()
      }
    }

    cy.get(".CodeMirror-code").last().type("!pip install -r requirements.txt")
    runCell()

    cy.get(".CodeMirror-code").last().type("import universaldatatool as udt")
    runCell()

    cy.get(".CodeMirror-code").last().type(
      `

ds = udt.Dataset(
    type="image_segmentation",
    image_paths=["/path/to/birds/good_bird.jpg","/path/to/birds/bird2.jpg"],
    labels=["good bird", "bad bird"]
)

      `.trim()
    )
    runCell()

    // TODO make sure there are no errors

    cy.get(".CodeMirror-code").last().type("ds.open()")
    runCell(false)
    cy.wait(1000)
    runCell(false)
  })
})
