import pytest
from pathlib import Path
import pyshacl
from rdflib import Graph

def validate_rdf(data_file: Path, shapes_file: Path) -> tuple[bool, str]:
    """Validate an RDF file against SHACL shapes. """
    data_graph = Graph()
    data_graph.parse(data_file)

    shapes_graph = Graph()
    shapes_graph.parse(shapes_file)

    validation_result = pyshacl.validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference='rdfs',
        abort_on_first=False,
        meta_shacl=True if shapes_file.name == "shacl-shacl.ttl" else False,
        debug=False
    )
    
    conforms, _, results_text = validation_result
    return conforms, results_text

def test_invalid_files():
    """Test that all files in the invalid directory fail validation."""
    invalid_dir = Path(__file__).parent / "invalid"
    shapes_file = Path(__file__).parent.parent / "shacl" / "premis-shacl.ttl"
    
    for invalid_file in invalid_dir.glob("*.ttl"):
        conforms, results = validate_rdf(invalid_file, shapes_file)
        assert not conforms, f"Expected validation to fail for {invalid_file.name}, but it passed"

def test_valid_files():
    """Test that all files in the valid directory validate correctly against SHACL."""
    valid_dir = Path(__file__).parent.parent / "valid"
    shapes_file = Path(__file__).parent.parent / "shacl" / "premis-shacl.ttl"
    
    for example_file in valid_dir.glob("*.ttl"):
        conforms, results = validate_rdf(example_file, shapes_file)
        assert conforms, f"SHACL validation failed for {example_file.name}:\n{results}"

def test_valid_examples():
    """Test that all examples validate correctly against SHACL."""
    examples_dir = Path(__file__).parent.parent / "examples"
    shapes_file = Path(__file__).parent.parent / "shacl" / "premis-shacl.ttl"
    
    for example_file in examples_dir.glob("*.ttl"):
        conforms, results = validate_rdf(example_file, shapes_file)
        assert conforms, f"SHACL validation failed for {example_file.name}:\n{results}"

def test_shacl_shapes():
    """Test that the SHACL shapes validate against meta-SHACL."""
    meta_shacl = Path(__file__).parent / "shacl" / "shacl-shacl.ttl"
    shapes_file = Path(__file__).parent.parent / "shacl" / "premis-shacl.ttl"
    
    conforms, results_text = validate_rdf(shapes_file, meta_shacl)
    assert conforms, f"Meta-SHACL validation failed for premis-shacl.ttl:\n{results_text}"
