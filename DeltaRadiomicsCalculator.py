import pandas as pd
import numpy as np

class DeltaRadiomicsCalculator:
    def __init__(self, pre_file_path, post_file_path,id_column):
        """
        初始化DeltaRadiomicsCalculator实例。
        
        :param pre_file_path: 预处理影像组学特征的Excel文件路径。
        :param post_file_path: 后处理影像组学特征的Excel文件路径。
        """
        self.pre_data = pd.read_excel(pre_file_path)
        self.post_data = pd.read_excel(post_file_path)
        self.id_column = id_column

    def _validate_data(self):
        if not set(self.pre_data.columns) == set(self.post_data.columns):
            raise ValueError("预处理和后处理数据的列不匹配")
        if not set(self.pre_data[self.id_column]) == set(self.post_data[self.id_column]):
            raise ValueError("预处理和后处理数据的ID不匹配")
            
    def calculate_and_save_to_sheets(self, output_file_path):
        self._validate_data()  # 验证数据一致性
        
        self.pre_data = self.pre_data.set_index(self.id_column)
        self.post_data = self.post_data.set_index(self.id_column)
        self.pre_data.sort_index(inplace=True)
        self.post_data.sort_index(inplace=True)
        
        epsilon = 1e-8

        diff = self.post_data - self.pre_data
        relative_delta = ( diff / (self.pre_data + epsilon) ) * 100
        delta_ratio = (self.post_data / (self.pre_data + epsilon)) * 100 

        dfs = {
            'Difference': diff.add_suffix('_diff'),
            'Relative Difference': relative_delta.add_suffix('_relative_diff'),
            'Delta Ratio': delta_ratio.add_suffix('_ratio'),
            'ABS difference': diff.abs().add_suffix('_abs_diff'),
        }

        for key in dfs:
            dfs[key].reset_index(inplace=True)

        with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
            for sheet_name, df in dfs.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Delta data saved to sheets in {output_file_path}")

# Example
# excel columns
  id,features_cols...

# pre_file_path = r'Feature_pre.xlsx'
# post_file_path = r'Feature_post.xlsx'
# output_file_path = r'Feature_delta.xlsx'

# calculator = DeltaRadiomicsCalculator(pre_file_path, post_file_path,'id')
# calculator.calculate_and_save_to_sheets(output_file_path)
