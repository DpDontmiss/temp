import argparse
import pandas as pd
import json
import sys
import os

def grade(submission_path, task_dir):
    try:
        # Load submission
        try:
            df_sub = pd.read_excel(submission_path, engine="odf")
        except Exception as e:
            return {"status": "fail", "message": f"Could not read submission file: {str(e)}"}
        
        # Load input (to verify against)
        input_path = os.path.join(task_dir, "cash_flows.ods")
        if not os.path.exists(input_path):
             return {"status": "error", "message": "Input file cash_flows.ods not found in task dir"}
             
        df_input = pd.read_excel(input_path, engine="odf")
        
        # Check if 'Reserve' column exists
        if "Reserve" not in df_sub.columns:
            return {"status": "fail", "message": "Column 'Reserve' not found in submission"}
            
        # Verify calculation: Reserve = Amount * 0.1
        if "Amount" not in df_input.columns:
             return {"status": "error", "message": "Input file missing 'Amount' column"}
             
        expected_reserves = df_input["Amount"] * 0.1
        
        # Check values with tolerance
        try:
            # We assume the row order is preserved.
            pd.testing.assert_series_equal(df_sub["Reserve"], expected_reserves, check_names=False, rtol=0.01)
        except AssertionError as e:
            return {"status": "fail", "message": f"Values do not match expected. {str(e)}"}
        except Exception as e:
             return {"status": "fail", "message": f"Error comparing values: {str(e)}"}
            
        return {"status": "pass"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--submission", required=True)
    parser.add_argument("--task-dir", required=True)
    args = parser.parse_args()
    
    result = grade(args.submission, args.task_dir)
    print(json.dumps(result))
