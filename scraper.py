from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.headless = False  # UI를 보면서 디버깅
driver = webdriver.Chrome(options=options)

driver.get("https://www.q-net.or.kr/crf005.do?id=crf00501&gSite=Q&gId=")  # 자격증 목록 페이지

try:
    # 검색창이 나타날 때까지 대기
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "topQuery"))  # ID 확인 필요
    )
    print("✅ 검색창 찾음!")

    # 검색 실행 (예제: '전기기사')
    search_box.send_keys("전기기사")
    search_box.submit()

    # 검색 결과 목록 대기
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "list_class_name"))  # 정확한 클래스명 확인 필요
    )
    
    # 검색 결과 가져오기
    cert_list = driver.find_elements(By.CLASS_NAME, "list_class_name")
    for cert in cert_list:
        print(cert.text)
    
except Exception as e:
    print(f"❌ 자격증 목록을 가져오는 데 실패: {e}")
finally:
    driver.quit()
