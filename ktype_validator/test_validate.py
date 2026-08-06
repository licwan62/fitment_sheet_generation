from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from validate import merge_by_key, validate_tables, write_iteration_input, write_outputs


class ValidatorTests(unittest.TestCase):
    def test_recursive_merge_uses_later_row_and_reports_conflict(self) -> None:
        header = (
            "id\tKtype\tNormalizedBodyStyle\tGeneration\tBodyCode\tDoors\t"
            "DIMENSION_GROUP_ID\tMatchConfidence\tNotes\tIterationStatus\n"
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "first.tsv"
            second = root / "second.tsv"
            first.write_text(
                header + "1\t1\tSedan\tG1\t\t4\tDG1\tHIGH\told\tREADY\n",
                encoding="utf-8",
            )
            second.write_text(
                header + "1\t1\tSedan\tG1\t\t4\tDG1\tHIGH\tnew\tREADY\n",
                encoding="utf-8",
            )
            merged, conflicts, all_rows, skipped = merge_by_key(
                [first, second], "mapping", "id"
            )
            self.assertEqual(merged[0]["Notes"], "new")
            self.assertEqual(len(conflicts["1"]), 2)
            self.assertEqual(len(all_rows), 2)
            self.assertEqual(skipped, [])

    def test_coverage_reference_and_conflict(self) -> None:
        source = [{"Ktype": "1"}, {"Ktype": "2"}, {"Ktype": "3"}]
        mapping = [
            {"id": "1", "Ktype": "1", "DIMENSION_GROUP_ID": "DG1", "IterationStatus": "READY"},
            {"id": "2", "Ktype": "2", "DIMENSION_GROUP_ID": "MISSING", "IterationStatus": "READY"},
            {"id": "3", "Ktype": "3", "DIMENSION_GROUP_ID": "DG2", "IterationStatus": "PENDING"},
        ]
        dimensions = [
            {"DIMENSION_GROUP_ID": "DG1", "LengthMM": "5000", "WidthMM": "2000", "HeightMM": "1800"},
            {"DIMENSION_GROUP_ID": "DG1", "LengthMM": "5000", "WidthMM": "2000", "HeightMM": "1800"},
            {"DIMENSION_GROUP_ID": "DG2", "LengthMM": "5000", "WidthMM": "2000", "HeightMM": "1800"},
            {"DIMENSION_GROUP_ID": "DG2", "LengthMM": "5200", "WidthMM": "2100", "HeightMM": "1900"},
        ]

        result = validate_tables(source, mapping, dimensions)
        self.assertEqual(result.source_total, 3)
        self.assertEqual(result.ready_total, 2)
        self.assertEqual(result.missing_ktypes, ["3"])
        self.assertEqual(len(result.missing_references), 1)
        self.assertEqual(set(result.dimension_conflicts), {"DG2"})
        self.assertFalse(result.passed)

    def test_outputs_are_always_created(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            report_dir = Path(temporary)
            result = validate_tables(
                [{"Ktype": "1"}],
                [{"id": "1", "Ktype": "1", "DIMENSION_GROUP_ID": "DG1", "IterationStatus": "READY"}],
                [{"DIMENSION_GROUP_ID": "DG1", "LengthMM": "1", "WidthMM": "2", "HeightMM": "3"}],
            )
            write_outputs(result, report_dir)
            self.assertIn("FINAL STATUS:\n\nPASS", (report_dir / "validation_report.txt").read_text())
            self.assertTrue((report_dir / "missing_ktype.txt").is_file())
            self.assertTrue((report_dir / "missing_dimension.txt").is_file())
            self.assertTrue((report_dir / "dimension_conflict.txt").is_file())

    def test_iteration_input_joins_missing_ktypes_to_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "all-eu.tsv"
            output = root / "iteration_input.tsv"
            source.write_text(
                "Make\tModel\tKtype\nA\tOne\t1\nB\tTwo\t2\nC\tThree\t3\n",
                encoding="utf-8",
            )
            count, unmatched = write_iteration_input(source, ["2", "3"], output)
            self.assertEqual(count, 2)
            self.assertEqual(unmatched, [])
            text = output.read_text(encoding="utf-8")
            self.assertIn("B\tTwo\t2", text)
            self.assertIn("C\tThree\t3", text)
            self.assertNotIn("A\tOne\t1", text)


if __name__ == "__main__":
    unittest.main()
