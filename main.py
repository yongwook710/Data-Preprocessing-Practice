import pandas as pd
import ast
import os  # 파일이 있는지 확인하기 위해 추가한 도구

# --- 1. 기능 정의 (이 부분은 아까랑 완전히 똑같습니다!) ---
def update_dataset_with_features(input_path, output_path):
    # 파일이 실제로 있는지 먼저 확인 (안전장치)
    if not os.path.exists(input_path):
        print(f"❌ 오류: '{input_path}' 파일이 없습니다! 넘어갑니다.")
        return

    print(f"\n📂 작업 시작... [{input_path}] 읽는 중")
    
    try:
        df = pd.read_csv(input_path)
        
        coefficients_list = []
        min_degrees_list = []
        max_degrees_list = []

        for index, row in df.iterrows():
            try:
                poly_data = ast.literal_eval(row['Jones_polynomial'])
                poly_data.sort(key=lambda x: x[0])
                
                degrees = [item[0] for item in poly_data]
                coeffs = [item[1] for item in poly_data]
                
                coefficients_list.append(coeffs)
                min_degrees_list.append(degrees[0])
                max_degrees_list.append(degrees[-1])
                
            except Exception as e:
                coefficients_list.append([])
                min_degrees_list.append(None)
                max_degrees_list.append(None)

        # 새 열 추가
        df['coefficients'] = coefficients_list
        df['min_degree'] = min_degrees_list
        df['max_degree'] = max_degrees_list

        # 저장
        df.to_csv(output_path, index=False)
        print(f"✅ 저장 완료 --> [{output_path}]")
        
    except Exception as e:
        print(f"💥 파일 처리 중 치명적인 오류 발생: {e}")

# --- 2. 실행 설정 ---
if __name__ == "__main__":
    
    target_numbers = [17, 18, 19]

    print(f"🚀 총 {len(target_numbers)}개의 파일 처리를 시작합니다")

    for num in target_numbers:
        # f-string: {num} 자리에 숫자가 자동으로 쏙쏙 들어갑니다.
        input_filename = f'data/finished_petalKnotTable_{num}.csv'
        output_filename = f'data/updated_knot_table_{num}.csv'
        
        # 함수 실행!
        update_dataset_with_features(input_filename, output_filename)

    print("\n🎉 모든 작업이 끝났습니다")