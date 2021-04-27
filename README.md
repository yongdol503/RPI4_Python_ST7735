# RPI4_Python_ST7735
Adafruit의 라이브러리를 기반으로 개선중인 ST7735_LCD 라이브러리  
https://github.com/cskau/Python_ST7735  
https://github.com/adafruit/Adafruit_Python_ILI9341

### RPI 커널 5.x.x 이상에서 비글본 블랙과 관련한 오류 발생 원인
- 문제가 발생하는 부분을 뜯어보니 커널 업데이트 이후 Adafruit_Python_GPIO 라이브러리 상에서 운영체제를 제대로 인식하지 못하는 것을 확인
- 현재 [Adafruit_Python_GPIO](https://github.com/adafruit/Adafruit_Python_GPIO) 라이브러리는 더이상 사용되지 않는 라이브러리임을 확인
- 무식하지만 응급조치로 Adafruit_Python_GPIO의 운영체제 인식 코드를 수정하여 무조건 라즈베리파이로 인식하게 수정하면 정상작동 됨
- 추후 Adafruit_Python_GPIO 대신 대체된 [Adafruit_Blinka](https://github.com/adafruit/Adafruit_Blinka) 라이브러리로 마이그레이션 할 계획
