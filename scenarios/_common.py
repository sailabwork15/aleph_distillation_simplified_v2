
from distill.column import ColumnSpec, DistillationColumn
from distill.io_utils import save_case_outputs


def run_case(out_dir, case_name, spec: ColumnSpec):
    col = DistillationColumn(spec)
    df, summary = col.simulate()
    paths = save_case_outputs(out_dir, case_name, df, summary)
    return df, summary, paths
