from moto_dimension_crawler.input_reader import read_input


def test_input_reader_preserves_supplied_input_id_for_resume_subset(tmp_path):
    path = tmp_path / "misses.tsv"
    path.write_text("INPUT_ID\tMAKE\tMODEL\n003072\tHonda\tCR125M\n", encoding="utf-8")
    cfg = {
        "input_columns": {
            "input_id": ["INPUT_ID"],
            "make": ["MAKE"],
            "model": ["MODEL"],
            "vehicle_type": ["车辆类型"],
        }
    }

    records = read_input(path, cfg)

    assert records[0].input_id == "003072"
