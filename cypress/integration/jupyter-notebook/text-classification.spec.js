context("Open UDT Text Classification Dataset", () => {
  it("log into jupyter notebook and create new notebook", () => {
    cy.visit("http://localhost:8888")
    cy.contains("Log in").click()
    cy.contains("New").click()

    cy.wait(1000)

    const win = cy.window().then(async (win) => {
      const {
        name,
      } = await win.Jupyter.new_notebook_widget.contents.new_untitled("", {
        type: "notebook",
      })
      cy.wait(500)
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

    cy.get(".CodeMirror-code").last().type("import universaldatatool as udt")
    runCell()

    cy.get(".CodeMirror-code").last().type(
      `

ds = udt.Dataset(
    type="text_classification",
    documents=["Hello World"],
    labels=["happy", "sad"]
)

      `.trim()
    )
    runCell()

    // TODO make sure there are no errors

    cy.get(".CodeMirror-code").last().type("ds.open()")
    runCell(false)

    cy.contains(".udt")
  })
})
