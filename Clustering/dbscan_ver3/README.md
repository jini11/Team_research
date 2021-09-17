#### 수정할 점
1. 최적의 eps, minpts 찾기


ver3 ->원본?  
ver3_2 -> 차원 축소 수정(t-SNE)  
ver4 -> 차원 축소 수정(UMAP)  

#### 현황
1. 최적의 eps, minpts는 4, 5
2. 어뷰징 리뷰들이 아웃라이어가 아니라 클러스터에 속해 있음
3. 텍스트 결과를 보면 긍정+짧은 문장들이 클러스터와 아웃라이어에 분포해 있는 상태(1~,-1)
4. 0번 클러스터에 긴 문장+정상리뷰+어뷰징리뷰가 섞여있는 상태

#### 앞으로 
1. 감성분석에서 분류한 어뷰징 리뷰들과 입력 리뷰의 텍스트 유사도를 이용한다.(어뷰징 리뷰들끼리의 유사도는 비슷할 것이라는 추측)
2. 0번 클러스터를 중심으로 감성분석 또는 추가적으로 클러스터링 실시한다.