import pandas as pd
import ast
import os

def update_dataset_with_features(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"❌ 오류: '{input_path}' 파일이 없습니다! 넘어갑니다.")
        return

    print(f"\n📂 작업 시작... [{input_path}] 읽는 중")
    
    try:
        df = pd.read_csv(input_path)
        
        # ... (데이터 처리 로직: coefficients, min_degree, max_degree 추출 부분은 동일) ...
        coefficients_list = []; min_degrees_list = []; max_degrees_list = []
        for index, row in df.iterrows():
            try:
                poly_data = ast.literal_eval(row['Jones_polynomial'])
                poly_data.sort(key=lambda x: x[0])
                degrees = [item[0] for item in poly_data]
                coeffs = [item[1] for item in poly_data]
                coefficients_list.append(coeffs); min_degrees_list.append(degrees[0]); max_degrees_list.append(degrees[-1])
            except:
                coefficients_list.append([]); min_degrees_list.append(None); max_degrees_list.append(None)

        df['coefficients'] = coefficients_list
        df['min_degree'] = min_degrees_list
        df['max_degree'] = max_degrees_list

        # 전체 결과 저장
        df.to_csv(output_path, index=False)
        print(f"✅ 전체 저장 완료 --> [{output_path}]")

        # 샘플 저장
        sample_path = output_path.replace('.csv', '_sample.csv')
        df.head(100).to_csv(sample_path, index=False)
        print(f"💡 샘플 생성 완료 --> [{sample_path}]")
        
    except Exception as e:
        print(f"💥 파일 처리 중 치명적인 오류 발생: {e}")

if __name__ == "__main__":
    target_numbers = [17, 18, 19]
    print(f"🚀 총 {len(target_numbers)}개의 파일 처리를 시작합니다")

    for num in target_numbers:
        input_filename = f'data/finished_petalKnotTable_{num}.csv'
        output_filename = f'data/updated_knot_table_{num}.csv'
        update_dataset_with_features(input_filename, output_filename)

    print("\n🎉 모든 작업이 끝났습니다.")