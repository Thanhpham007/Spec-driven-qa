# Feature Specification: XOmni Password Login QC

**Feature Branch**: `001-password-login`

**Created**: 2026-08-31

**Status**: Draft

**Input**: User description: "Tạo tài liệu đặc tả tự động hóa kiểm thử chất lượng (QC) cho tính năng Đăng nhập bằng mật khẩu của XOmni. Ứng dụng cần kiểm thử đã có sẵn. Không được sửa đổi ứng dụng. User story: Là người dùng hệ thống AI Workforce, tôi muốn đăng nhập bằng email và mật khẩu để có thể truy cập ứng dụng. IN SCOPE: đăng nhập bằng mật khẩu; thông tin hợp lệ; mật khẩu không hợp lệ; email bắt buộc; mật khẩu bắt buộc. OUT OF SCOPE: OTP email, Google, Facebook, Microsoft, Apple, đăng ký, quên mật khẩu. REQ-LOGIN-001..005 và AC-LOGIN-001..005."

## Clarifications

### Session 2026-08-31

- Q: Khi nguyên văn thông báo lỗi chưa xác định, phiên bản này MUST xác minh điều gì cho đăng nhập thất bại? → A: Xác minh đăng nhập thất bại và có trạng thái hoặc thông báo lỗi nhìn thấy được; không yêu cầu nguyên văn lỗi khớp từng chữ.

## User Scenarios & Testing *(mandatory)*

Tài liệu này mô tả hành vi **đã giao** của trang Đăng nhập bằng mật khẩu trên XOmni để kiểm thử chất lượng. Ứng dụng đã có sẵn và **không** được sửa đổi. Chỉ các hành vi ghi trong yêu cầu và tiêu chí chấp nhận dưới đây mới là oracle kiểm thử.

### User Story 1 - Xem trang Đăng nhập khi chưa xác thực (Priority: P1)

Là người dùng hệ thống AI Workforce chưa xác thực, tôi mở trang Đăng nhập và thấy đủ các thành phần cần thiết để đăng nhập bằng email và mật khẩu.

**Why this priority**: Không có trang Đăng nhập thì không thể kiểm tra bất kỳ luồng đăng nhập nào.

**Independent Test**: Người dùng chưa xác thực mở trang Đăng nhập và xác nhận các nhãn/trường được liệt kê trong AC-LOGIN-001.

**Acceptance Scenarios**:

1. **AC-LOGIN-001** — **Given** người dùng chưa xác thực, **When** người dùng mở trang Đăng nhập, **Then** hiển thị "Đăng nhập", **And** hiển thị Email, **And** hiển thị Mật khẩu, **And** hiển thị "Tiếp tục".

---

### User Story 2 - Đăng nhập thành công với thông tin hợp lệ (Priority: P1)

Là người dùng hệ thống AI Workforce, tôi nhập email và mật khẩu hợp lệ rồi chọn "Tiếp tục" để truy cập ứng dụng.

**Why this priority**: Đây là giá trị nghiệp vụ chính của tính năng đăng nhập bằng mật khẩu.

**Independent Test**: Trên trang Đăng nhập, nhập email và mật khẩu hợp lệ, chọn "Tiếp tục", xác nhận đăng nhập thành công theo AC-LOGIN-002.

**Acceptance Scenarios**:

1. **AC-LOGIN-002** — **Given** có email và mật khẩu hợp lệ, **When** người dùng nhấp vào "Tiếp tục", **Then** đăng nhập thành công, **And** người dùng rời khỏi trang Đăng nhập.

---

### User Story 3 - Từ chối mật khẩu không hợp lệ (Priority: P2)

Là người dùng hệ thống AI Workforce, tôi không được truy cập ứng dụng khi mật khẩu không hợp lệ.

**Why this priority**: Bảo vệ truy cập; độc lập với luồng thành công.

**Independent Test**: Trên trang Đăng nhập, dùng email hợp lệ và mật khẩu không hợp lệ, chọn "Tiếp tục", xác nhận thất bại theo AC-LOGIN-003.

**Acceptance Scenarios**:

1. **AC-LOGIN-003** — **Given** có email hợp lệ và mật khẩu không hợp lệ, **When** người dùng nhấp vào "Tiếp tục", **Then** đăng nhập không thành công, **And** hiển thị trạng thái hoặc thông báo lỗi có thể nhìn thấy. Phiên bản này MUST NOT yêu cầu nguyên văn thông báo khớp từng chữ.

---

### User Story 4 - Email là trường bắt buộc (Priority: P2)

Là người dùng hệ thống AI Workforce, tôi không thể gửi đăng nhập khi thiếu Email.

**Why this priority**: Ràng buộc trường bắt buộc; độc lập với mật khẩu sai.

**Independent Test**: Để trống Email, gửi biểu mẫu Đăng nhập, xác nhận thất bại và thông báo kiểm tra Email theo AC-LOGIN-004.

**Acceptance Scenarios**:

1. **AC-LOGIN-004** — **Given** trường Email để trống, **When** người dùng gửi biểu mẫu Đăng nhập, **Then** đăng nhập không thành công, **And** hiển thị thông báo kiểm tra (validation) cho Email.

---

### User Story 5 - Mật khẩu là trường bắt buộc (Priority: P2)

Là người dùng hệ thống AI Workforce, tôi không thể gửi đăng nhập khi thiếu Mật khẩu.

**Why this priority**: Ràng buộc trường bắt buộc; độc lập với Email trống.

**Independent Test**: Để trống Mật khẩu, gửi biểu mẫu Đăng nhập, xác nhận thất bại và thông báo kiểm tra Mật khẩu theo AC-LOGIN-005.

**Acceptance Scenarios**:

1. **AC-LOGIN-005** — **Given** trường Mật khẩu để trống, **When** người dùng gửi biểu mẫu Đăng nhập, **Then** đăng nhập không thành công, **And** hiển thị thông báo kiểm tra (validation) cho Mật khẩu.

---

### Edge Cases

Chỉ các biên đã nêu trong tiêu chí chấp nhận:

- Email hợp lệ kết hợp mật khẩu không hợp lệ: đăng nhập thất bại và có trạng thái hoặc thông báo lỗi nhìn thấy được; không đối chiếu nguyên văn từng chữ (AC-LOGIN-003).
- Email trống khi gửi biểu mẫu: đăng nhập thất bại và có thông báo kiểm tra cho Email (AC-LOGIN-004).
- Mật khẩu trống khi gửi biểu mẫu: đăng nhập thất bại và có thông báo kiểm tra cho Mật khẩu (AC-LOGIN-005).

Không mở rộng thêm biên (ví dụ định dạng email, khóa tài khoản, cả hai trường trống cùng lúc, hay nội dung trang sau khi rời Đăng nhập) trừ khi được bổ sung vào đặc tả này.

## Requirements *(mandatory)*

### Functional Requirements

- **REQ-LOGIN-001**: Hệ thống MUST hiển thị trang Đăng nhập cho người dùng chưa xác thực.
- **REQ-LOGIN-002**: Người dùng có email và mật khẩu hợp lệ MUST đăng nhập thành công.
- **REQ-LOGIN-003**: Người dùng có thông tin đăng nhập không hợp lệ MUST NOT được phép truy cập ứng dụng. Với AC-LOGIN-003, kiểm thử MUST xác nhận đăng nhập thất bại và có trạng thái hoặc thông báo lỗi nhìn thấy được; MUST NOT bắt buộc nguyên văn lỗi chính xác từng chữ khi nội dung đó chưa được chốt.
- **REQ-LOGIN-004**: Email MUST là trường bắt buộc.
- **REQ-LOGIN-005**: Mật khẩu MUST là trường bắt buộc.

Ánh xạ yêu cầu → tiêu chí chấp nhận (không thêm hành vi):

| Requirement     | Acceptance Criteria |
|-----------------|---------------------|
| REQ-LOGIN-001   | AC-LOGIN-001        |
| REQ-LOGIN-002   | AC-LOGIN-002        |
| REQ-LOGIN-003   | AC-LOGIN-003        |
| REQ-LOGIN-004   | AC-LOGIN-004        |
| REQ-LOGIN-005   | AC-LOGIN-005        |

### Key Entities

- **Phiên chưa xác thực**: Người dùng chưa đăng nhập; được phép xem trang Đăng nhập.
- **Thông tin đăng nhập bằng mật khẩu**: Email và mật khẩu. "Hợp lệ" nghĩa là cặp giá trị mà hệ thống chấp nhận cho đăng nhập thành công. "Mật khẩu không hợp lệ" nghĩa là email hợp lệ nhưng mật khẩu không đúng cặp đó.
- **Trang Đăng nhập**: Màn hình có "Đăng nhập", Email, Mật khẩu, và "Tiếp tục" như AC-LOGIN-001.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% lần mở trang Đăng nhập với người dùng chưa xác thực, người dùng nhìn thấy đủ bốn yếu tố: "Đăng nhập", Email, Mật khẩu, và "Tiếp tục".
- **SC-002**: 100% lần gửi "Tiếp tục" với email và mật khẩu hợp lệ, đăng nhập thành công và người dùng không còn ở trang Đăng nhập.
- **SC-003**: 100% lần gửi "Tiếp tục" với email hợp lệ và mật khẩu không hợp lệ, người dùng không truy cập được ứng dụng và thấy trạng thái hoặc thông báo lỗi có thể nhìn thấy (không đo bằng việc khớp nguyên văn từng chữ).
- **SC-004**: 100% lần gửi biểu mẫu khi Email trống, đăng nhập không thành công và có thông báo kiểm tra cho Email.
- **SC-005**: 100% lần gửi biểu mẫu khi Mật khẩu trống, đăng nhập không thành công và có thông báo kiểm tra cho Mật khẩu.
- **SC-006**: Phạm vi kiểm thử chất lượng của tính năng này gồm đúng năm kịch bản trên (AC-LOGIN-001 đến AC-LOGIN-005) và không đưa thêm hành vi ngoài phạm vi vào oracle.

## Assumptions

- Ứng dụng XOmni (hệ thống AI Workforce) đã triển khai và là đối tượng kiểm thử; công việc này không thay đổi ứng dụng.
- Tồn tại sẵn tài khoản với email và mật khẩu hợp lệ để kiểm tra REQ-LOGIN-002 / AC-LOGIN-002; giá trị bí mật không nằm trong đặc tả này.
- Nhãn người dùng nhìn thấy đúng như tiêu chí chấp nhận: "Đăng nhập", Email, Mật khẩu, "Tiếp tục".
- "Đăng nhập thành công" được xác nhận bằng việc người dùng rời khỏi trang Đăng nhập. Đặc tả không quy định màn hình đích sau đăng nhập.
- Phiên bản này: nguyên văn thông báo lỗi chưa xác định. Oracle AC-LOGIN-003 MUST là (1) đăng nhập thất bại và (2) trạng thái hoặc thông báo lỗi nhìn thấy được; MUST NOT yêu cầu khớp từng chữ. "Thông báo kiểm tra" (AC-LOGIN-004, AC-LOGIN-005) vẫn chỉ yêu cầu có chỉ báo kiểm tra tương ứng, không quy định nguyên văn.
- REQ-LOGIN-003 trong phạm vi này được kiểm chứng bằng trường hợp mật khẩu không hợp lệ (AC-LOGIN-003), không bằng các phương thức đăng nhập khác.
- "Gửi biểu mẫu Đăng nhập" tương đương hành động người dùng dùng để nộp Email/Mật khẩu trên trang đó (cùng ý với chọn "Tiếp tục" khi các trường được điền).

## Out of Scope

Các hạng mục sau **MUST NOT** được đưa vào đặc tả, kịch bản, hay oracle kiểm thử của tính năng này:

- Đăng nhập bằng OTP qua email
- Đăng nhập bằng Google
- Đăng nhập bằng Facebook
- Đăng nhập bằng Microsoft
- Đăng nhập bằng Apple
- Đăng ký tài khoản
- Quên mật khẩu
- Mọi hành vi nghiệp vụ không được ghi trong REQ-LOGIN-001..005 và AC-LOGIN-001..005
