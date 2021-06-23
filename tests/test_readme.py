def test_readme() -> None:
    with open("README.md", encoding="UTF-8") as f:
        readme_contents = f.read()
    assert "Usage" in readme_contents
