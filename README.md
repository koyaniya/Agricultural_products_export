# Agricultural_products_export
1. Summary : This project aims to analyze the export of agricultural products from South Korea to other countries. While South Korea is typically associated with the export of high-tech products and heavy industrial goods, this project seeks to explore the current state of the country’s agricultural exports.

2. Data Source: Data set was provided by 농산물전문생산단지 (Specialized Agricultural Production Complex)
This dataset contains information about the export of agricultural products from South Korea between 2018 and 2025. The data are organized by year and month of export. It includes the name of the agricultural product, the association that provided the product, the quantity exported, the destination country, and the name of the exporting company, among other details.

3. Data Details :
   상품 컬럼 정보
 - delv_yr : 	출고연도
 - delv_mm : 출고월
 - hsmp_sno : 단지일련번호
 - hsmp_nm : 단지명
 - fmhs_code : 농가코드
 - pdlt_nm : 품목명
 - delv_qyt : 출고수량
 - epot_etps_nm : 수출업체명
 - ntn_nm : 국가명
 - etl_ldg_dt : 적재일시

4. Analysis flow:
 1) Download the row date from https://kadx.co.kr/opmk/frn/pmumkproductDetail/PMU_89774b1b-0830-4346-86c7-f60e46b79e29/5#
 2) Cleaning and preparing the data for analysis (see python script)
 3) Making vizualization with Tableau (see Tableau dasboard)
