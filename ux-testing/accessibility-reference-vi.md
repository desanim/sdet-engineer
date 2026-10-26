# Thư viện tham khảo Accessibility QA — giải thích từng nguồn

Tài liệu này giải thích cụ thể từng nguồn trong bộ tham khảo: nguồn nói về gì, QA dùng vào việc gì, nên đọc phần nào trước và cần lưu ý giới hạn nào. Đây là bản hướng dẫn học bằng tiếng Việt; tên và đường dẫn tài liệu gốc được giữ nguyên để bạn tra cứu.

## Bản đồ học nhanh

| Khi cần... | Mở nguồn này trước |
|---|---|
| Hiểu accessibility và nhóm người dùng | [WAI Fundamentals](https://www.w3.org/WAI/fundamentals/) |
| Biết tiêu chí nào cần kiểm tra | [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) |
| Xác nhận chính xác yêu cầu chuẩn | [WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/) |
| Kiểm tra widget có bàn phím hoạt động thế nào | [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) |
| Học kỹ thuật HTML và accessibility tree | [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility) |
| Quét lỗi tự động | [axe](https://www.deque.com/axe/), [WAVE](https://wave.webaim.org/), [Lighthouse](https://developer.chrome.com/docs/lighthouse/accessibility/) |
| Kiểm tra trải nghiệm đọc màn hình trên Windows | [NVDA](https://www.nvaccess.org/) |
| Lập phương pháp audit theo phạm vi | [WCAG-EM](https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/) |
| Tra tiêu chuẩn Trung Quốc | [GB/T 37668-2019 trên cơ sở dữ liệu SAMR](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=35ECC696805C1A67C93B74FB6D0D8EFB) |

## 1. Chuẩn WCAG và tài liệu W3C

### 1.1 WCAG 2 Overview — trang tổng quan

**Nguồn:** [W3C WAI — WCAG 2 Overview](https://www.w3.org/WAI/standards-guidelines/wcag/)

**Nguồn này có gì:** Giải thích WCAG là gì, mối quan hệ giữa các phiên bản 2.0, 2.1, 2.2, cách dùng các tài liệu hỗ trợ và mối liên hệ với những tiêu chuẩn khác.

**QA dùng khi nào:** Dùng lúc bắt đầu dự án audit để xác định nhóm chuẩn đang áp dụng và lúc cần hiểu WCAG nằm ở đâu trong hệ thống tiêu chuẩn. Đây là điểm vào để biết tài liệu nào là bản chuẩn, tài liệu nào là hướng dẫn đọc.

**Nên tập trung:** Cấu trúc nguyên tắc POUR, cấp độ A/AA/AAA, phiên bản 2.2 và phần liên hệ với ISO/IEC, EN 301 549.

**Giới hạn:** Đây là trang tổng quan, không đủ để kết luận một trang đạt hay không đạt tiêu chí cụ thể. Khi viết finding, mở Quick Reference hoặc tiêu chuẩn gốc.

### 1.2 How to Meet WCAG 2 — Quick Reference

**Nguồn:** [W3C WAI — WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)

**Nguồn này có gì:** Danh sách các success criteria, mức A/AA/AAA, mô tả ngắn, kỹ thuật hỗ trợ và các bộ lọc theo chủ đề.

**QA dùng khi nào:** Đây là tài liệu tra cứu thường xuyên khi chuyển yêu cầu thành bước kiểm thử. Ví dụ: cần kiểm tra focus visible, label form, error identification, contrast hoặc reflow thì tìm tiêu chí liên quan, đọc nguyên văn rồi lập test oracle.

**Cách dùng:**
1. Chọn WCAG 2.2 và mức mục tiêu của dự án.
2. Lọc theo chủ đề hoặc tìm từ khóa/SC.
3. Đọc yêu cầu normative, không chỉ đọc phần tóm tắt.
4. Viết lại thành điều kiện kiểm tra quan sát được.
5. Ghi rõ trang, state, phương pháp và bằng chứng.

**Giới hạn:** Quick Reference giúp tìm và hiểu tiêu chí nhưng không tự xác định sản phẩm, trang hay state nào thuộc phạm vi audit. Techniques là cách thực hiện gợi ý; một kỹ thuật cụ thể không phải lựa chọn duy nhất để đạt tiêu chí.

### 1.3 WCAG 2.2 Standard — bản chuẩn đầy đủ

**Nguồn:** [W3C Recommendation — WCAG 2.2](https://www.w3.org/TR/WCAG22/)

**Nguồn này có gì:** Bản đặc tả chính thức của WCAG 2.2, gồm nguyên tắc, guideline, success criteria, yêu cầu conformance và định nghĩa.

**QA dùng khi nào:** Dùng để xác minh cách hiểu khi finding có tranh luận, khi cần trích chính xác tiêu chí, hoặc khi cần hiểu điều kiện conformance và các ngoại lệ.

**Cách dùng:** Ghi đúng phiên bản, số SC, tên SC và level. Ví dụ: “WCAG 2.2, 2.4.7 Focus Visible, AA”. Chỉ gán một lỗi cho SC nếu có bằng chứng cho thấy yêu cầu đó thực sự không được đáp ứng.

**Lưu ý phiên bản:** WCAG 2.2 trở thành ISO/IEC 40500:2025 dựa trên bản WCAG 2.2 tháng 10/2023. Khi báo cáo cho sản phẩm hoặc hợp đồng cụ thể, xác nhận bản chuẩn được yêu cầu; đừng tự thay WCAG 2.1 bằng 2.2 nếu văn bản áp dụng nói khác.

### 1.4 WCAG-EM — phương pháp đánh giá

**Nguồn:** [W3C WAI — Website Accessibility Conformance Evaluation Methodology (WCAG-EM)](https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/)

**Nguồn này có gì:** Hướng dẫn xác định phạm vi, khám phá website, chọn mẫu đại diện, kiểm tra, ghi nhận kết quả và báo cáo đánh giá WCAG.

**QA dùng khi nào:** Khi chuyển từ “thử vài trang” sang audit có phương pháp và có thể giải thích độ phủ. Dùng để lập inventory, xác định các trang quan trọng, chọn mẫu theo user journey và ghi rõ giới hạn.

**Giới hạn:** Phương pháp chọn mẫu không đồng nghĩa với việc đã kiểm tra toàn bộ hệ thống. Nếu audit không bao phủ đầy đủ trang/state cần thiết, kết luận phải giới hạn theo phạm vi đã kiểm tra.

## 2. ARIA, HTML và component tương tác

### 2.1 ARIA Authoring Practices Guide (APG)

**Nguồn:** [W3C WAI — ARIA APG](https://www.w3.org/WAI/ARIA/apg/)

**Nguồn này có gì:** Mẫu tương tác cho tabs, dialog, accordion/disclosure, menu button, combobox, carousel và nhiều widget khác; mô tả semantics, trạng thái và thao tác bàn phím mong đợi.

**QA dùng khi nào:** Khi sản phẩm có component động hoặc custom widget. Dùng bảng keyboard interaction trong APG để tạo kiểm thử: phím nào di chuyển focus, phím nào chọn, Escape làm gì, focus được trả về đâu, screen reader nhận tên/role/state ra sao.

**Cách học hiệu quả:** Chọn widget đang có trong app; đọc pattern; tạo ma trận phím và kết quả kỳ vọng; kiểm tra bằng bàn phím và screen reader. Đừng học thuộc mọi widget khi chưa gặp chúng.

**Giới hạn:** APG là hướng dẫn thiết kế pattern, không thay thế WCAG và không có nghĩa copy ví dụ là tự động đảm bảo accessibility. Một menu điều hướng thông thường có thể cần link và list ngữ nghĩa, không nhất thiết là ARIA menu widget.

### 2.2 WAI-ARIA 1.2 — đặc tả kỹ thuật

**Nguồn:** [W3C — WAI-ARIA 1.2](https://www.w3.org/TR/wai-aria-1.2/)

**Nguồn này có gì:** Định nghĩa roles, states, properties và cách nội dung tương tác được trình bày cho accessibility API.

**QA dùng khi nào:** Khi kiểm tra role/name/state của custom component, khi xem accessibility tree hoặc khi cần xác minh cách dùng thuộc tính ARIA.

**Cần nhớ:** ARIA bổ sung semantics; nó không tự tạo hành vi bàn phím, focus management hay validation. Một nút giả làm bằng div có role button vẫn cần hỗ trợ bàn phím và hành vi đúng. Native HTML thường là lựa chọn an toàn hơn.

**Giới hạn:** Đây là đặc tả kỹ thuật khó đọc với người mới; không nên bắt đầu học accessibility bằng cách đọc toàn bộ tài liệu này. Bắt đầu với HTML semantic và APG, rồi tra spec khi có câu hỏi cụ thể.

### 2.3 MDN Accessibility

**Nguồn:** [MDN — Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)

**Nguồn này có gì:** Giải thích cách HTML, CSS, JavaScript và trình duyệt ảnh hưởng đến accessibility; nhiều bài gắn trực tiếp với code và accessibility tree.

**QA dùng khi nào:** Khi cần hiểu nguyên nhân kỹ thuật đằng sau finding hoặc trao đổi với developer về name, role, state, label, landmarks hay focus.

**Giới hạn:** MDN là tài liệu giáo dục kỹ thuật, không phải chuẩn conformance. Khi cần quyết định pass/fail WCAG, quay lại tiêu chí gốc.

## 3. Nguồn học nền tảng và checklist

### 3.1 WAI Accessibility Fundamentals

**Nguồn:** [W3C WAI — Accessibility Fundamentals](https://www.w3.org/WAI/fundamentals/)

**Nguồn này có gì:** Giới thiệu accessibility, người khuyết tật, assistive technology, inclusive design và các nguyên tắc nền tảng.

**QA dùng khi nào:** Ở giai đoạn đầu để chuyển tư duy từ “check giao diện” sang “kiểm tra người dùng có thể tiếp cận thông tin và hoàn thành mục tiêu không”. Tạo liên hệ giữa rào cản và test idea.

**Sản phẩm nên tạo:** Bảng “nhu cầu/ngữ cảnh → rào cản có thể gặp → hành vi cần kiểm tra”. Ví dụ: người chỉ dùng bàn phím → không thể tới nút thanh toán → kiểm tra thứ tự focus, focus visible và khả năng kích hoạt.

### 3.2 The A11Y Project

**Nguồn:** [The A11Y Project](https://www.a11yproject.com/)

**Nguồn này có gì:** Bài giải thích ngắn, checklist và liên kết học tập được viết theo hướng dễ bắt đầu.

**QA dùng khi nào:** Dùng để ôn một chủ đề, tạo checklist khởi đầu hoặc tìm cách diễn giải đơn giản cho khái niệm khó.

**Giới hạn:** Không coi checklist cộng đồng là bằng chứng conformance. Kiểm tra lại mỗi yêu cầu với WCAG/APG hoặc tài liệu chính thức.

### 3.3 WebAIM

**Nguồn:** [WebAIM](https://webaim.org/)

**Nguồn này có gì:** Bài viết thực hành về accessibility, screen reader, form, contrast và kỹ thuật web. Có [Contrast Checker](https://webaim.org/resources/contrastchecker/).

**QA dùng khi nào:** Học cách giải thích contrast, label, screen reader và các lỗi thường gặp; dùng contrast checker để sàng lọc cặp màu.

**Giới hạn:** Máy tính contrast không biết chữ đó có đủ lớn, đậm, có trạng thái hover/focus khác, hoặc hình ảnh có chữ hay không. Kết quả cần được đánh giá trong đúng ngữ cảnh thiết kế và tiêu chí WCAG.

### 3.4 Deque University

**Nguồn:** [Deque University](https://dequeuniversity.com/)

**Nguồn này có gì:** Khóa học và bài học có cấu trúc về accessibility, WCAG, ARIA và screen reader. Một số nội dung có thể miễn phí, một số cần tài khoản hoặc trả phí.

**QA dùng khi nào:** Dùng khi muốn học theo bài có thứ tự thay vì tự ghép nhiều bài viết; tốt cho việc củng cố quy trình audit và cách kiểm tra.

**Giới hạn:** Nội dung học không thay thế thực hành trên website thật; kiểm tra điều kiện truy cập và mức cập nhật của từng khóa.

## 4. Công cụ tự động

### 4.1 axe DevTools và axe-core

**Nguồn:** [Deque axe](https://www.deque.com/axe/) | [axe-core trên GitHub](https://github.com/dequelabs/axe-core)

**Dùng để:** Quét một số lỗi có thể phát hiện từ DOM/accessibility tree; tích hợp vào browser workflow hoặc automated test.

**QA áp dụng:** Chạy scan trên từng state quan trọng, lưu tool/version, mở từng finding, xác nhận nó tái hiện và ghi vị trí chính xác. Nếu đội dùng Playwright, có thể tích hợp axe-core để phát hiện regression tự động.

**Không dùng để:** Kết luận “đạt WCAG AA” chỉ vì không có lỗi scan. Tool không thể tự hiểu mọi nội dung thay thế, chất lượng hướng dẫn, thứ tự hợp lý, khả năng hoàn thành task hay mọi lỗi screen reader.

### 4.2 WAVE

**Nguồn:** [WAVE Web Accessibility Evaluation Tool](https://wave.webaim.org/)

**Dùng để:** Hiển thị overlay trực quan về một số lỗi, cảnh báo, cấu trúc heading, landmark, label và contrast.

**QA áp dụng:** Dùng khi khám phá nhanh một trang để thấy các điểm cần điều tra; đối chiếu với DOM và thao tác thực tế.

**Giới hạn:** Icon warning không luôn là lỗi; cần đọc đúng ngữ cảnh. Overlay cũng không thay thế kiểm tra keyboard/screen reader.

### 4.3 Lighthouse Accessibility

**Nguồn:** [Chrome Lighthouse accessibility audits](https://developer.chrome.com/docs/lighthouse/accessibility/)

**Dùng để:** Có tín hiệu kiểm tra nhanh trong quy trình Chrome/CI và phát hiện một số lỗi kỹ thuật.

**QA áp dụng:** Lưu report theo build để so sánh regression; dùng từng audit fail làm đầu mối kiểm tra.

**Giới hạn:** Điểm số không phải tỷ lệ accessibility và không chứng minh WCAG conformance. Lighthouse chỉ đánh giá tập quy tắc tự động mà nó hỗ trợ.

### Nguyên tắc dùng automation

Không có tỷ lệ phần trăm duy nhất đúng cho mọi sản phẩm về số lỗi mà automation tìm ra. Tỷ lệ thay đổi theo công cụ, rule, markup và loại lỗi. Hãy ghép scan với keyboard, screen reader, zoom/reflow, kiểm tra nội dung và đánh giá thủ công có chuyên môn.

## 5. Screen reader và kiểm tra thủ công

### 5.1 NVDA

**Nguồn/tải:** [NV Access — NVDA](https://www.nvaccess.org/)

**Dùng để:** Kiểm tra trải nghiệm screen reader trên Windows; thường dùng cùng Firefox hoặc Chrome theo tổ hợp trình duyệt mà dự án hỗ trợ.

**QA cần luyện:**
- Đọc theo thứ tự nội dung và headings.
- Di chuyển qua landmarks, links, buttons, form fields.
- Xác minh accessible name, role, state, required và error.
- Thực hiện user journey hoàn chỉnh, gồm modal, autocomplete, validation và kết quả động.
- Quan sát lúc focus và virtual cursor khác nhau.

**Giới hạn:** Một lần nghe trang chủ không đủ để đánh giá. Ghi rõ tổ hợp NVDA + browser/version và task đã kiểm tra vì hành vi có thể khác theo nền tảng.

### 5.2 VoiceOver

**Nguồn:** [Apple — VoiceOver User Guide](https://support.apple.com/guide/voiceover/welcome/mac)

**Dùng để:** Kiểm tra sản phẩm trên macOS/iOS trong các tổ hợp hỗ trợ, thường với Safari.

**QA cần luyện:** Di chuyển qua nội dung, rotor/headings, controls, form, dialog, announcement và thao tác touch screen nếu audit mobile.

**Giới hạn:** Nếu bạn chỉ có Windows, ghi rõ VoiceOver chưa được kiểm tra thay vì suy đoán kết quả. Không suy rộng kiểm thử một cặp OS/browser sang mọi nền tảng.

## 6. Chuẩn pháp lý và thị trường

### 6.1 WCAG 2.2

Là bộ hướng dẫn kỹ thuật của W3C với các success criteria cấp A, AA, AAA. QA cần được giao rõ phiên bản và level mục tiêu. Level AA là mục tiêu phổ biến trong nhiều dự án, nhưng áp dụng pháp lý phụ thuộc sản phẩm, thị trường và văn bản liên quan.

### 6.2 ISO/IEC 40500:2025

W3C xác nhận ISO/IEC 40500:2025 tương ứng với phiên bản WCAG 2.2 tháng 10/2023. Khi tài liệu dự án ghi ISO hoặc WCAG, xác minh chính xác phiên bản được viện dẫn; các bản cập nhật khác có thể chưa thuộc cùng ấn bản ISO.

### 6.3 EN 301 549 và EAA tại EU

- [EUR-Lex — EAA summary](https://eur-lex.europa.eu/EN/legal-content/summary/accessibility-of-products-and-services.html)
- [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj/eng)

EAA áp dụng từ 28/06/2025 cho một số nhóm sản phẩm và dịch vụ được nêu trong Directive. Phạm vi, ngoại lệ và cách thực hiện nằm trong văn bản EU và luật chuyển hóa của quốc gia thành viên. EN 301 549 là tiêu chuẩn ICT liên quan; cần kiểm tra phiên bản được hợp đồng hoặc quy định áp dụng viện dẫn. Không kết luận mọi website đều có cùng nghĩa vụ.

### 6.4 Section 508 tại Hoa Kỳ

**Nguồn:** [Section508.gov — Applicability and Conformance Requirements](https://www.section508.gov/develop/applicability-conformance/)

Revised 508 Standards tham chiếu WCAG 2.0 cấp A và AA cho ICT thuộc phạm vi. QA nên xác minh sản phẩm có thuộc đối tượng Section 508 không, tài liệu/phiên bản nào áp dụng, và yêu cầu cụ thể của agency hoặc hợp đồng. Không gọi đây là “luật WCAG 2.2” một cách chung chung.

### 6.5 Trung Quốc: GB/T và chính sách

- [SAMR — hồ sơ chính thức GB/T 37668-2019](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=35ECC696805C1A67C93B74FB6D0D8EFB)
- [MIIT — 工信部联管函〔2020〕146号](https://www.miit.gov.cn/jgsj/xgj/wjfb/art/2020/art_457a63f75df24c749ea2a8a44c713161.html)
- [MIIT — 专项行动方案 về ứng dụng internet thích ứng người cao tuổi và accessibility](https://www.miit.gov.cn/jgsj/xgj/wjfb/art/2020/art_18a8b1029f724afc8b31264fcd0f4106.html)

GB/T 37668-2019 có tên 《信息技术 互联网内容无障碍可访问性技术要求与测试方法》, áp dụng kỹ thuật cho nội dung internet và phương pháp kiểm tra; hồ sơ SAMR ghi tiêu chuẩn hiện hành và ngày thực hiện 01/03/2020. Ký hiệu GB/T là tiêu chuẩn quốc gia dạng khuyến nghị; không tự diễn giải thành nghĩa vụ pháp lý cho mọi công ty.

Văn bản 2020 và kế hoạch hành động giúp hiểu chính sách và bối cảnh triển khai tại Trung Quốc. Hãy kiểm tra ngày, đối tượng, giai đoạn và văn bản thay thế nếu cần đánh giá nghĩa vụ hiện tại. Phần pháp lý nên được xác nhận với người phụ trách compliance tại thị trường đó.

## 7. Tổ chức và cộng đồng chuyên môn Trung Quốc

### 7.1 信息无障碍研究会 (SIAA / Accessibility Research Association)

**Nguồn:** [siaa.org.cn](https://www.siaa.org.cn/)

**Có thể tìm:** Bài viết, hoạt động cộng đồng, hội nghị, nghiên cứu và tài liệu thực hành về thông tin không rào cản, thiết kế thích ứng người cao tuổi và kinh nghiệm tại Trung Quốc.

**QA dùng khi nào:** Tìm bối cảnh và ví dụ thực tế ở thị trường Trung Quốc; tìm thuật ngữ tiếng Trung và chủ đề đang được cộng đồng quan tâm.

**Giới hạn:** Không xem website tổ chức như bản tiêu chuẩn pháp quy. Xác nhận tác giả, ngày đăng, nguồn gốc số liệu và đối chiếu yêu cầu với tiêu chuẩn/văn bản chính thức.

### 7.2 联谛信息无障碍 (Link Accessibility)

**Nguồn:** [linkacce.com](https://www.linkacce.com/)

**Có thể tìm:** Dịch vụ đánh giá, tư vấn, case study doanh nghiệp và kinh nghiệm cải thiện accessibility/age-friendly design.

**QA dùng khi nào:** Xem cách nhà cung cấp chuyên môn trình bày quy trình, deliverable, phân loại vấn đề và thực hiện dự án.

**Giới hạn:** Đây là nhà cung cấp dịch vụ, không phải cơ quan chuẩn hóa. Case study là ví dụ triển khai, không phải bằng chứng độc lập rằng một phương pháp luôn đúng.

### 7.3 Juejin và Zhihu

**Nguồn:** [Juejin](https://juejin.cn/) | [Zhihu](https://www.zhihu.com/)

**Từ khóa tiếng Trung nên dùng:**
- 无障碍 / 信息无障碍 — accessibility / information accessibility
- 适老化 — thiết kế thích ứng người cao tuổi
- WCAG / ARIA — tên chuẩn và kỹ thuật
- 屏幕阅读器 — screen reader
- 键盘无障碍 — keyboard accessibility
- 焦点管理 — focus management
- 表单无障碍 — accessible forms

**QA dùng khi nào:** Tìm bài chia sẻ từ team kỹ thuật hoặc ví dụ lỗi/thực hành tại các sản phẩm Trung Quốc.

**Giới hạn:** Bài cộng đồng có thể cũ, thiếu nguồn hoặc chỉ đúng với một framework. Dùng nó để hình thành giả thuyết và câu hỏi; xác minh kết luận bằng tiêu chuẩn và thử nghiệm thực tế.

## 8. Thứ tự học đề xuất cho QA có kinh nghiệm manual testing

1. **WAI Fundamentals:** hiểu người dùng và rào cản.
2. **WCAG Overview + Quick Reference:** nắm cấu trúc và chọn tiêu chí liên quan đến task.
3. **Keyboard + HTML semantic:** thực hành focus, link/button, heading, form labels.
4. **NVDA:** kiểm tra task thật và ghi lại announcement/interaction.
5. **APG:** tra pattern khi gặp widget phức tạp; viết keyboard matrix.
6. **axe/WAVE/Lighthouse:** quét, xác nhận, phân biệt finding thật và cảnh báo.
7. **WCAG-EM + audit template:** xác định scope, sample và ghi giới hạn.
8. **Nguồn thị trường:** chỉ học Section 508, EAA/EN 301 549, hoặc tiêu chuẩn Trung Quốc theo thị trường công việc.

## 9. Cách ghi một nguồn trong portfolio

Khi viện dẫn tài liệu trong audit report, ghi đủ:

- Tên và phiên bản chuẩn.
- Số và tên success criterion (nếu kết luận vi phạm).
- Link tới nguồn gốc.
- Trang/state và bước tái hiện.
- Môi trường: OS, browser, viewport, input, screen reader/version.
- Bằng chứng và giới hạn của lần kiểm tra.

Không dùng logo của công cụ, điểm Lighthouse hoặc “không có lỗi axe” để tuyên bố sản phẩm đạt WCAG. Công cụ là một phần bằng chứng; audit phải mô tả phạm vi và phương pháp.

## Tài liệu liên quan trong repo

- [Thư viện tiếng Anh](accessibility-reference.md)
- [Lộ trình Accessibility QA 16 tuần](a11y-16-week-roadmap.md)
- [Mẫu báo cáo audit accessibility](accessibility-audit-template.md)
