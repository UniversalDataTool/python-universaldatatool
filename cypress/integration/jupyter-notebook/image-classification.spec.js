context("Open UDT Image Classification Dataset", () => {
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

  const runCell = (andInsert = true) => {
    cy.wait(100)
    cy.get(".dropdown-toggle").contains("Cell").click()
    if (andInsert) {
      cy.contains("Run Cells and Insert Below").click()
    } else {
      cy.contains("Run Cells").click()
    }
  }

  it("should be able to import udt and open a dataset", () => {
    cy.get(".CodeMirror-code").last().type("import universaldatatool as udt")
    runCell()

    cy.get(".CodeMirror-code").last().type(
      `

ds = udt.Dataset(
    type="image_classification",
    image_paths=["/home/jovyan/cypress/integration/jupyter-notebook/bird.jpg"],
    labels=["good bird", "bad bird"]
)

      `.trim()
    )
    runCell()

    // TODO make sure there are no errors

    cy.get(".CodeMirror-code").last().type("ds.open()")
    runCell()

    cy.contains(".udt")
  })

  it("should be able to save output", () => {
    cy.contains("good bird (g)").click()
    cy.get(".CodeMirror-code").last().type(
      `
      ds.samples[0]

          `.trim()
    )
    runCell()
    cy.contains("annotation: good bird")
  })
})
