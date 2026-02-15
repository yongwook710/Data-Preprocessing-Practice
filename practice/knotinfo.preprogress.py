import pandas as pd
import sympy
from sympy import symbols, parse_expr

def parse_polynomial_string(poly_str):
    """
    입력: "t+ t^3-t^4" (문자열)
    출력: (1, 4, [1, 0, 1, -1])  -> (최소차수, 최대차수, 계수리스트)
    """
    try:
        # 1. 데이터가 비어있으면 패스
        if pd.isna(poly_str):
            return None, None, []

        # 2. 파이썬이 이해할 수 있게 기호 변경 (^ -> **)
        # 예: t^3 -> t**3
        s = str(poly_str).replace('^', '**')
        
        # 3. 수식 해석 (SymPy 사용)
        t = symbols('t')
        expr = parse_expr(s)
        
        # 4. 식을 전개해서 {항: 계수} 딕셔너리로 변환
        # 예: t+ t^3-t^4 -> {t: 1, t**3: 1, t**4: -1}
        expr = expr.expand()
        coeff_dict = expr.as_coefficients_dict()
        
        # 5. 차수(degree)별로 계수 정리하기
        parsed_coeffs = {}
        for term, coeff in coeff_dict.items():
            # 차수 알아내기 (상수는 0, t는 1, t^n은 n)
            if term == 1: 
                d = 0
            elif term.is_Symbol: 
                d = 1
            elif term.is_Pow: 
                d = int(term.args[1]) # 지수 부분 가져오기
            else:
                d = 0 # 예외 처리
            
            parsed_coeffs[d] = int(coeff)
            
        # 6. 중간에 빈 차수(0) 채워넣기 (Dense 형태)
        if not parsed_coeffs:
            return None, None, []

        min_deg = min(parsed_coeffs.keys())
        max_deg = max(parsed_coeffs.keys())
        
        dense_coeffs = []
        for d in range(min_deg, max_deg + 1):
            # 해당 차수에 값이 없으면 0을 넣음
            dense_coeffs.append(parsed_coeffs.get(d, 0))
            
        return dense_coeffs, min_deg, max_deg

    except Exception as e:
        print(f"⚠️ 해석 실패 ({poly_str}): {e}")
        return None, None, []

# --- 실행 부분 ---
if __name__ == "__main__":
    # 1. 파일 읽기
    input_file = 'data/knotinfo.csv'  # 파일 이름 확인!
    output_file = 'data/updated_knotinfo.csv'
    
    print(f"📂 [{input_file}] 파일을 처리합니다...")
    df = pd.read_csv(input_file)
    
    # 2. 데이터 처리
    coefficients = []
    min_degrees = []
    max_degrees = []

    for index, row in df.iterrows():
        # Jones 컬럼을 읽어서 처리
        coeffs, min_d, max_d = parse_polynomial_string(row['Jones'])
        
        coefficients.append(coeffs)
        min_degrees.append(min_d)
        max_degrees.append(max_d)

    # 3. 새로운 열 추가
    df['coefficients'] = coefficients
    df['min_degree'] = min_degrees
    df['max_degree'] = max_degrees

    # 4. 저장하기
    df.to_csv(output_file, index=False)
    
    print(f"✅ 저장 완료! [{output_file}] 파일을 확인해보세요.")
    print("\n--- 결과 미리보기 ---")
    print(df.head())