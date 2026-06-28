# ☕ 테크살롱 (Tech Salon)
개발 과정에서 마주한 고민, 경험, 인사이트를 딥다이브하여 발표하고 토론하는 스터디입니다.

# 🎯 스터디 목표
- 개발 과정에서의 시행착오와 해결 경험을 함께 나눈다.
- 발표를 통해 자신의 생각을 구조화하고 전달하는 능력을 기른다.
- 서로의 경험을 통해 시야를 넓히며 함께 성장한다.

# 🗣️ 진행 방식
- 발표 시간: 10분 ± 5분
- 발표 후 자유 Q&A 및 토론 진행
- 발표 주제 제한 없음
  - 미션/프로젝트 관련 문제 해결 경험
  - 기술적 의사결정, 성능 개선 등

# 🤝 스터디 문화
- 질문과 토론을 자유롭게 나눈다.
- 서로의 경험을 존중하며, 정답보다는 사고 과정, 관점 등을 중요하게 생각한다.
- 발표 후 익명 피드백을 통해 좋았던 점과 개선할 점을 나눈다.

# 👥 멤버
| ![](https://github.com/Jiihyun.png?size=150) | ![](https://github.com/Uechann.png?size=150) | ![](https://github.com/softmoca.png?size=150) | ![](https://github.com/sangjun121.png?size=150) | ![](https://github.com/MODUGGAGI.png?size=150) | ![](https://github.com/2Jaeheon.png?size=150) | ![](https://github.com/quddaz.png?size=150) |
|:----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| [러키](https://github.com/Jiihyun) | [마이찬](https://github.com/Uechann) | [모카](https://github.com/softmoca) | [샤를](https://github.com/sangjun121) | [스타크](https://github.com/MODUGGAGI) | [초록](https://github.com/2Jaeheon) | [쿠다](https://github.com/quddaz) |


## 발표 자료 업로드 방법

<details>
<summary>발표 자료 업로드 순서 보기</summary>

<br>

발표 자료는 GitHub Issue 템플릿을 통해 업로드합니다.  
이슈를 생성하면 GitHub Actions가 자동으로 PDF 저장, 썸네일 생성, README 발표 아카이브 갱신까지 처리합니다.

### 1. 발표 영상 업로드

발표 영상이 있다면 먼저 YouTube에 영상을 업로드한 뒤 영상 URL을 복사합니다.

> 발표 영상 URL은 선택 항목입니다.  
> 영상이 아직 없다면 비워두고 PDF만 먼저 업로드해도 됩니다.

### 2. 이슈 템플릿 선택

저장소 상단 메뉴에서 `Issues` → `New issue`를 클릭합니다.

이후 **스터디자료 업로드** 템플릿을 선택합니다.

### 3. 이슈 제목 확인

이슈 제목은 기본값인 `[업로드]`를 그대로 둡니다.

처리가 완료되면 자동으로 아래 형식으로 변경됩니다.

```text
[업로드] Level N - 발표자 / 제목
```

### 4. 발표 정보 입력

아래 항목을 입력합니다.

| 항목 | 설명 |
| --- | --- |
| `Level` | 숫자만 입력합니다. 예) `1` |
| `발표자` | 발표자 닉네임을 입력합니다. |
| `제목` | 발표 제목을 입력합니다. |
| `발표 영상 URL` | YouTube 영상 URL을 입력합니다. 영상이 없다면 비워둡니다. |
| `PDF 파일` | 발표 자료 PDF를 드래그 앤 드롭합니다. |

예시:

```text
Level: 1
발표자: 모카
제목: 컨트롤러의 오해, 그리고 서비스 계층
발표 영상 URL: https://youtube.com/...
PDF 파일: 발표 자료 PDF 업로드
```

### 5. 이슈 생성

모든 항목을 입력한 뒤 `Create` 버튼을 클릭합니다.

이슈가 생성되면 GitHub Actions가 자동으로 실행됩니다.
처리에는 약 30초 정도 소요될 수 있습니다.

### 6. 처리 완료 확인

처리가 완료되면 다음 작업이 자동으로 수행됩니다.

1. PDF 파일 저장
2. PDF 첫 페이지 기반 썸네일 생성
3. 발표 데이터 갱신
4. README 발표 아카이브 갱신
5. 자동 커밋
6. 이슈에 완료 댓글 작성
7. 이슈 자동 close

업로드가 끝난 뒤 README의 발표 아카이브에 자료가 정상적으로 반영되었는지 확인합니다.

</details>

## 발표 자료 수정 방법

README 발표 아카이브는 발표 데이터로부터 자동 생성됩니다. 기존 발표 항목의 발표자, 제목, 발표 영상 URL, PDF 파일을 바꾸려면 README 아카이브 행을 직접 수정하지 말고 **스터디자료 수정** 이슈를 생성합니다.

<details>
<summary>발표 자료 수정 순서 보기</summary>

<br>

저장소 상단 메뉴에서 `Issues` → `New issue`를 클릭한 뒤 **스터디자료 수정** 템플릿을 선택합니다.

아래 항목을 입력합니다.

| 항목 | 설명 |
| --- | --- |
| `Level` | 수정할 발표가 등록된 Level을 숫자만 입력합니다. 예) `1` |
| `현재 발표자` | README 발표 아카이브에 현재 등록된 발표자명을 정확히 입력합니다. |
| `현재 제목` | README 발표 아카이브에 현재 등록된 발표 제목을 정확히 입력합니다. |
| `새 발표자` | 발표자명을 바꿀 때만 입력합니다. 비워두면 기존 값이 유지됩니다. |
| `새 제목` | 발표 제목을 바꿀 때만 입력합니다. 비워두면 기존 값이 유지됩니다. |
| `발표 영상 URL` | 영상 URL을 바꿀 때 입력합니다. 비워두면 기존 값이 유지되고, `없음`을 입력하면 영상 URL이 제거됩니다. |
| `PDF 파일` | PDF를 교체할 때만 새 PDF 파일을 드래그 앤 드롭합니다. 비워두면 기존 PDF 파일이 유지됩니다. |

예시:

```text
Level: 1
현재 발표자: 모카
현재 제목: 컨트롤러의 오해, 그리고 서비스 계층
새 발표자:
새 제목: 컨트롤러의 오해, 그리고 서비스 계층 다시 보기
발표 영상 URL: 없음
PDF 파일:
```

이슈가 생성되면 GitHub Actions가 현재 등록된 `Level`, `현재 발표자`, `현재 제목`과 정확히 일치하는 발표 항목을 찾아 입력한 값으로 갱신합니다. 처리 완료 후 README 발표 아카이브는 발표 데이터 기준으로 다시 생성됩니다.

</details>

# 📚 발표 아카이브

## Level 1

| 발표 자료(클릭 시 확인 가능) | 발표 정보 |
|---|---|
| <div align="center"><a href="https://github.com/woowacourse-study/2026-be-tech-salon/blob/main/docs/level1/%5B%EB%9F%AC%ED%82%A4%5D%20%EA%B7%B8%20%EC%B6%94%EC%83%81%ED%99%94%2C%20%EC%A0%95%EB%A7%90%20%ED%95%84%EC%9A%94%ED%95%9C%EA%B0%80%EC%9A%94.pdf"><img src="https://github.com/woowacourse-study/2026-be-tech-salon/raw/main/images/level1/%5B%EB%9F%AC%ED%82%A4%5D%20%EA%B7%B8%20%EC%B6%94%EC%83%81%ED%99%94%2C%20%EC%A0%95%EB%A7%90%20%ED%95%84%EC%9A%94%ED%95%9C%EA%B0%80%EC%9A%94.png" width="300"/></a></div> | **발표자:** 러키<br>**발표 주제:** 그 추상화, 정말 필요한가요?<br>**발표 영상:** <a href="https://youtu.be/jo9TWgOb6Is?si=VZWFR2u1bEMqcxMV">🎥 발표 영상</a> |
| <div align="center"><a href="https://github.com/woowacourse-study/2026-be-tech-salon/blob/main/docs/level1/%EC%BB%A8%ED%8A%B8%EB%A1%A4%EB%9F%AC%EC%9D%98%20%EC%98%A4%ED%95%B4%2C%20%EA%B7%B8%EB%A6%AC%EA%B3%A0%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EA%B3%84%EC%B8%B5.pdf"><img src="https://github.com/woowacourse-study/2026-be-tech-salon/raw/main/images/level1/%EC%BB%A8%ED%8A%B8%EB%A1%A4%EB%9F%AC%EC%9D%98%20%EC%98%A4%ED%95%B4%2C%20%EA%B7%B8%EB%A6%AC%EA%B3%A0%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EA%B3%84%EC%B8%B5.png" width="300"/></a></div> | **발표자:** 모카<br>**발표 주제:** 컨트롤러의 오해, 그리고 서비스 계층<br>**발표 영상:** <a href="https://www.youtube.com/watch?v=VCWZsh5dPEc">🎥 발표 영상</a> |
| <div align="center"><a href="https://github.com/woowacourse-study/2026-be-tech-salon/blob/main/docs/level1/HikariCP%20%EB%82%B4%EB%B6%80%20%EC%BD%94%EB%93%9C%20%ED%8C%8C%ED%97%A4%EC%B9%98%ED%82%A4.pdf"><img src="https://github.com/woowacourse-study/2026-be-tech-salon/raw/main/images/level1/HikariCP%20%EB%82%B4%EB%B6%80%20%EC%BD%94%EB%93%9C%20%ED%8C%8C%ED%97%A4%EC%B9%98%ED%82%A4.png" width="300"/></a></div> | **발표자:** 스타크<br>**발표 주제:** HikariCP 내부 코드 파헤치기<br>**발표 영상:** <a href="https://youtu.be/nEQ6to3Y-w4?si=QlUcPQk30UBN_1wK">🎥 발표 영상</a> |
| <div align="center"><a href="https://github.com/woowacourse-study/2026-be-tech-salon/blob/main/docs/level1/DriverManager%20VS%20Datasource.pdf"><img src="https://github.com/woowacourse-study/2026-be-tech-salon/raw/main/images/level1/DriverManager%20VS%20Datasource.png" width="300"/></a></div> | **발표자:** 초록<br>**발표 주제:** DriverManager VS Datasource<br>**발표 영상:** <a href="https://youtu.be/J1PnyYITyXc">🎥 발표 영상</a> |
| <div align="center"><a href="https://github.com/woowacourse-study/2026-be-tech-salon/blob/main/docs/level1/%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EC%86%8C%EC%8B%B1%EA%B3%BC%20CQRS%20%EC%A0%81%EC%9A%A9%20%EC%8B%9C%ED%96%89%20%EC%B0%A9%EC%98%A4.pdf"><img src="https://github.com/woowacourse-study/2026-be-tech-salon/raw/main/images/level1/%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EC%86%8C%EC%8B%B1%EA%B3%BC%20CQRS%20%EC%A0%81%EC%9A%A9%20%EC%8B%9C%ED%96%89%20%EC%B0%A9%EC%98%A4.png" width="300"/></a></div> | **발표자:** 샤를<br>**발표 주제:** 이벤트 소싱과 CQRS 적용 시행 착오<br>**발표 영상:** <a href="https://youtu.be/fA0wkkxsE4U?si=BJEMvcyHQfGywf7w">🎥 발표 영상</a> |
| <div align="center"><a href="https://github.com/woowacourse-study/2026-be-tech-salon/blob/main/docs/level1/%ED%9D%A9%EC%96%B4%EC%A7%84%20%E3%80%8E%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%E3%80%8F%20%EC%86%8D%EC%9D%98%20%EB%8F%99%EC%9D%98%EC%96%B4%EC%99%80%20%EC%9D%B8%EA%B3%BC%EA%B4%80%EA%B3%84.pdf"><img src="https://github.com/woowacourse-study/2026-be-tech-salon/raw/main/images/level1/%ED%9D%A9%EC%96%B4%EC%A7%84%20%E3%80%8E%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%E3%80%8F%20%EC%86%8D%EC%9D%98%20%EB%8F%99%EC%9D%98%EC%96%B4%EC%99%80%20%EC%9D%B8%EA%B3%BC%EA%B4%80%EA%B3%84.png" width="300"/></a></div> | **발표자:** 마이찬<br>**발표 주제:** 흩어진 『오브젝트』 속의 동의어와 인과관계<br>**발표 영상:** <a href="https://youtu.be/tSDc0mXE6l0">🎥 발표 영상</a> |
| <div align="center"><a href="https://github.com/woowacourse-study/2026-be-tech-salon/blob/main/docs/level1/%EC%9A%B0%EC%95%84%ED%95%9C%20Null%20%EC%B2%98%EB%A6%AC.pdf"><img src="https://github.com/woowacourse-study/2026-be-tech-salon/raw/main/images/level1/%EC%9A%B0%EC%95%84%ED%95%9C%20Null%20%EC%B2%98%EB%A6%AC.png" width="300"/></a></div> | **발표자:** 쿠다<br>**발표 주제:** 우아한 Null 처리<br>**발표 영상:** <a href="https://www.youtube.com/watch?v=sROB9Wgzv0c">🎥 발표 영상</a> |

<br>

## Level 2

| 발표 자료(클릭 시 확인 가능) | 발표 정보 |
|---|---|
| <div align="center"><a href="https://github.com/woowacourse-study/2026-be-tech-salon/blob/main/docs/level2/%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EA%B0%80%20%EB%8D%B0%EB%93%9C%EB%9D%BD%EC%9D%84%20%EC%B2%98%EB%A6%AC%ED%95%98%EB%8A%94%20%EB%B0%A9%EC%8B%9D.pdf"><img src="https://github.com/woowacourse-study/2026-be-tech-salon/raw/main/images/level2/%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EA%B0%80%20%EB%8D%B0%EB%93%9C%EB%9D%BD%EC%9D%84%20%EC%B2%98%EB%A6%AC%ED%95%98%EB%8A%94%20%EB%B0%A9%EC%8B%9D.png" width="300"/></a></div> | **발표자:** 샤를<br>**발표 주제:** 데이터베이스가 데드락을 처리하는 방식<br>**발표 영상:** <a href="https://youtu.be/Pwp8wB9iTws?si=pZBrhK52BrYm9ynF">🎥 발표 영상</a> |

<br>
