USE MASTER
GO

USE pt
IF EXISTS (SELECT * FROM sysdatabases WHERE name='khoaluantotnghiep')
		DROP DATABASE khoaluantotnghiep
GO

CREATE DATABASE khoaluantotnghiep
GO

USE khoaluantotnghiep
GO

--------------------------------
--------------------------------
--------------------------------
CREATE TABLE TinhTP ( Id_TinhTP nvarchar(10),
					  Ten_TinhTP nvarchar(50),
					  PRIMARY KEY (Id_TinhTP)
					  )
GO

CREATE TABLE QuanHuyen ( Id_QuanHuyen nvarchar(10),
						 Ten_QuanHuyen nvarchar(50),
						 Id_TinhTP nvarchar(10),
						 PRIMARY KEY (Id_QuanHuyen),
						 FOREIGN KEY (Id_TinhTP) REFERENCES TinhTP(Id_TinhTP) 
						 )
GO

CREATE TABLE PhuongXa ( Id_PhuongXa nvarchar(10),
						Ten_PhuongXa nvarchar(50),
						Id_QuanHuyen nvarchar(10),
						PRIMARY KEY (Id_PhuongXa),
						FOREIGN KEY (Id_QuanHuyen) REFERENCES QuanHuyen(Id_QuanHuyen) 
						)
GO

--------------------------------
--------------------------------
--------------------------------
CREATE TABLE NganhNghe ( Id_NganhNghe nvarchar(10),
						 Ten_NganhNghe nvarchar(100),
						 PRIMARY KEY (Id_NganhNghe)
						 )
GO

CREATE TABLE ChuyenNganh ( Id_ChuyenNganh nvarchar(10),
						   Ten_ChuyenNganh nvarchar(100),
						   Id_NganhNghe nvarchar(10),
						   PRIMARY KEY (Id_ChuyenNganh),
						   FOREIGN KEY (Id_NganhNghe) REFERENCES NganhNghe(Id_NganhNghe)
						   )
GO

CREATE TABLE ViTriChuyenMon ( Id_ViTri nvarchar(10),
							  Ten_ViTri nvarchar(100),
							  Id_ChuyenNganh nvarchar(10),
							  PRIMARY KEY (Id_ViTri),
							  FOREIGN KEY (Id_ChuyenNganh) REFERENCES ChuyenNganh(Id_ChuyenNganh)
							  )
GO

--------------------------------
--------------------------------
--------------------------------
CREATE TABLE TrinhDo ( Id_TrinhDo nvarchar(10),
					  Ten_TrinhDo nvarchar(50),
					  PRIMARY KEY (Id_TrinhDo)
					  )
GO

CREATE TABLE CapBac ( Id_CapBac nvarchar(10),
					  Ten_CapBac nvarchar(50),
					  PRIMARY KEY (Id_CapBac)
					  )
GO



CREATE TABLE KyNang ( Id_KyNang nvarchar(10),
					  Ten_KyNang nvarchar(50),
					  PRIMARY KEY (Id_KyNang)
					  )
GO

CREATE TABLE KyNangMem ( Id_KyNangMem nvarchar(10),
					  Ten_KyNangMem nvarchar(50),
					  PRIMARY KEY (Id_KyNangMem)
					  )
GO

CREATE TABLE ChuyenMon ( Id_ChuyenMon nvarchar(10),
					  Ten_ChuyenMon nvarchar(50),
					  PRIMARY KEY (Id_ChuyenMon)
					  )
GO


CREATE TABLE NgoaiNgu ( Id_NgoaiNgu nvarchar(10),
					  Ten_NgoaiNgu nvarchar(50),
					  PRIMARY KEY (Id_NgoaiNgu)
					  )
GO

--------------------------------
--------------------------------
--------------------------------

CREATE TABLE CongTy ( Id_Congty nvarchar(10),
					  Ten_CongTy nvarchar(100),
					  SDT_CongTy nvarchar(10),
					  DiaChi_CongTy nvarchar(100),
					  Email_CongTy nvarchar(50),
					  MaSoThue_CongTy nvarchar(50),
					  PRIMARY KEY (Id_CongTy),
					  )
GO

CREATE TABLE NhaTuyenDung ( Id_NhaTuyenDung nvarchar(10),
							Ten_NhaTuyenDung nvarchar(50),
							GioiTinh_NhaTuyenDung nvarchar(10),
							SDT_NhaTuyenDung nvarchar(10),
							DiaChi_NhaTuyenDung nvarchar(10),
							Email_NhaTuyenDung nvarchar(50),
							Id_Congty nvarchar(10),
							PRIMARY KEY (Id_NhaTuyenDung),
							FOREIGN KEY (Id_Congty) REFERENCES CongTy(Id_Congty)
							)
GO

CREATE TABLE UngVien ( Id_UngVien nvarchar(10),
					   Ten_UngVien nvarchar(50),
					   GioiTinh_UngVien nvarchar(10),
					   SDT_UngVien nvarchar(10),
					   DiaChi_UngVien nvarchar(10),
					   Email_UngVien nvarchar(50),
					   PRIMARY KEY (Id_UngVien),
					   FOREIGN KEY (DiaChi_UngVien) REFERENCES PhuongXa(Id_PhuongXa)
					   )
GO

CREATE TABLE CongViec ( Id_CongViec nvarchar(10),
						Ten_CongViec nvarchar(100),
						Id_NhaTuyenDung nvarchar(10),
						---
						ViTri_CongViec nvarchar(10),
						---ky nang
						---ky nang mem
						KhuVuc_CongViec nvarchar(10),
						MucLuong_CongViec int,
						CapBac_CongViec nvarchar(10),
						DoTuoi_CongViec int,
						KinhNghiem_CongViec int,
						GioiTinh_CongViec nvarchar(10),
						TrinhDo_CongViec nvarchar(10),
						ChuyenMon_CongViec nvarchar(10),
						NgoaiNgu_CongViec nvarchar(10),
						PRIMARY KEY (Id_CongViec),
						FOREIGN KEY (Id_NhaTuyenDung) REFERENCES NhaTuyenDung(Id_NhaTuyenDung),
						FOREIGN KEY (ViTri_CongViec) REFERENCES ViTriChuyenMon(Id_ViTri),
						FOREIGN KEY (KhuVuc_CongViec) REFERENCES PhuongXa(Id_PhuongXa),
						FOREIGN KEY (CapBac_CongViec) REFERENCES CapBac(Id_CapBac),
						FOREIGN KEY (TrinhDo_CongViec) REFERENCES TrinhDo(Id_TrinhDo),
						FOREIGN KEY (ChuyenMon_CongViec) REFERENCES ChuyenMon(Id_ChuyenMon),
						FOREIGN KEY (NgoaiNgu_CongViec) REFERENCES NgoaiNgu(Id_NgoaiNgu),
						)
GO
--------------------------------
--------------------------------
--------------------------------
CREATE TABLE FilterUV (
    Id_FilterUV INT IDENTITY(1,1) PRIMARY KEY,
    Id_UngVien NVARCHAR(10),
    ThoiGian DATETIME,
    
    -- Thông tin công việc tìm kiếm
    ViTri NVARCHAR(200), 
    ChuyenNganh NVARCHAR(200),
    NganhNghe NVARCHAR(200),
    PhuongXa NVARCHAR(200),
    QuanHuyen NVARCHAR(200),
    TinhTP NVARCHAR(200),
    CapBac NVARCHAR(200),
    TrinhDo NVARCHAR(200),
    ChuyenMon NVARCHAR(200),
    NgoaiNgu NVARCHAR(200),
    
    -- Yêu cầu về mức lương và kinh nghiệm
    ThuNhapMin INT,
    ThuNhapMax INT,
    TuoiMin INT,
    TuoiMax INT,
    KinhNghiem INT,
    GioiTinh NVARCHAR(10),

    -- Kỹ năng chuyên môn và kỹ năng mềm
    KyNang NVARCHAR(200),
    KyNangMem NVARCHAR(200),

    FOREIGN KEY (Id_UngVien) REFERENCES UngVien(Id_UngVien)
);
GO


CREATE TABLE ChiTietKyNang ( Id_CTKN int IDENTITY(1,1),
							 Id_CongViec nvarchar(10),
							 Id_KyNang nvarchar(10),
							 PRIMARY KEY (Id_CTKN),
							 FOREIGN KEY (Id_CongViec) REFERENCES CongViec(Id_CongViec),
							 FOREIGN KEY (Id_KyNang) REFERENCES KyNang (Id_KyNang)
							 )
GO

CREATE TABLE ChiTietKyNangMem ( Id_CTKNM int IDENTITY(1,1),
							 Id_CongViec nvarchar(10),
							 Id_KyNangMem nvarchar(10),
							 PRIMARY KEY (Id_CTKNM),
							 FOREIGN KEY (Id_CongViec) REFERENCES CongViec(Id_CongViec),
							 FOREIGN KEY (Id_KyNangMem) REFERENCES KyNangMem (Id_KyNangMem)
							 )
GO


CREATE TABLE TaiKhoan ( id nvarchar(50),
						TaiKhoan nvarchar(100),
						MatKhau nvarchar(100),
						QuyenHan nvarchar(50),
						Id_NguoiDung nvarchar(10),
						PRIMARY KEY (id),
						FOREIGN KEY (Id_NguoiDung) REFERENCES UngVien (Id_UngVien),
						)
GO

CREATE TABLE LichSu (
    id NVARCHAR(10),       -- ID người dùng
    create_at DATETIME DEFAULT GETDATE(), -- Ngày tạo
    cauhoi NVARCHAR(MAX),  -- Câu hỏi của người dùng
    cautraloi NVARCHAR(MAX), -- Câu trả lời của AI
    PRIMARY KEY (id, create_at),  -- Khóa chính gồm ID và thời gian
	FOREIGN KEY (id) REFERENCES UngVien(Id_UngVien)
);
GO
SELECT *
FROM LichSu
DELETE LichSu WHERE id='user_123'

-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
SET DATEFORMAT dmy;

INSERT INTO TinhTP VALUES (N'TTP01',N'Hồ Chí Minh'),--
				          (N'TTP02',N'Đà Nẵng'),--
						  (N'TTP03',N'Hà Nội')--
GO

INSERT INTO QuanHuyen VALUES (N'QH01',N'Bình Thạnh',N'TTP01'),
							 (N'QH02',N'Quận 1',N'TTP01'),
							 (N'QH03',N'Quận 6',N'TTP01'),---
							 (N'QH04',N'Hải Châu',N'TTP02'),
							 (N'QH05',N'Thanh Khê',N'TTP02'),
							 (N'QH06',N'Sơn Trà',N'TTP02'),---
							 (N'QH07',N'Ba Đình',N'TTP03'),
							 (N'QH08',N'Cầu Giấy',N'TTP03'),
							 (N'QH09',N'Hoàn Kiếm',N'TTP03')---
GO

INSERT INTO PhuongXa VALUES (N'PX01',N'Phường 1',N'QH01'),
							(N'PX02',N'Phường 2',N'QH01'),---
							(N'PX03',N'Phường 3',N'QH02'),
							(N'PX04',N'Phường 4',N'QH02'),---
							(N'PX05',N'Phường 5',N'QH03'),
							(N'PX06',N'Phường 6',N'QH03'),---
							(N'PX07',N'Phường 7',N'QH04'),---
							(N'PX08',N'Phường 8',N'QH05'),
							(N'PX09',N'Phường 9',N'QH05'),---
							(N'PX10',N'Phường 10',N'QH06'),
							(N'PX11',N'Phường 11',N'QH06'),---
							(N'PX12',N'Phường 12',N'QH07'),
							(N'PX13',N'Phường 13',N'QH07'),---
							(N'PX14',N'Phường 14',N'QH08'),
							(N'PX15',N'Phường 15',N'QH08'),---
							(N'PX16',N'Phường 16',N'QH09'),
							(N'PX17',N'Phường 17',N'QH09')---
GO


-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
INSERT INTO NganhNghe VALUES (N'NgNge01',N'Công nghệ Thông tin'),--
							 (N'NgNge02',N'Logistics'),--
							 (N'NgNge03',N'Giáo dục/Đào tạo'),--
							 (N'NgNge04',N'Sản xuất'),--
							 (N'NgNge05',N'Điện/Điện tử')--
GO

INSERT INTO ChuyenNganh VALUES (N'ChNg01',N'Software Engineering',N'NgNge01'),
							   (N'ChNg02',N'Artificial Intelligent (AI)',N'NgNge01'),
							   (N'ChNg03',N'Data Science',N'NgNge01'),---
							   (N'ChNg04',N'Xuất Nhập Khẩu',N'NgNge02'),
							   (N'ChNg05',N'Vận tải',N'NgNge02'),---
							   (N'ChNg06',N'Giáo viên',N'NgNge03'),
							   (N'ChNg07',N'Thể chất',N'NgNge03'),---
							   (N'ChNg08',N'Gia công cơ khí',N'NgNge04'),
							   (N'ChNg09',N'Thiết kế/Chế tạo',N'NgNge04'),---
							   (N'ChNg10',N'Điện/Tự động hóa',N'NgNge05'),
							   (N'ChNg11',N'Điện tử/Phần cứng',N'NgNge05')---
GO

INSERT INTO ViTriChuyenMon VALUES (N'VTChM01',N'Backend Developer',N'ChNg01'),
								  (N'VTChM02',N'Fullstack Developer',N'ChNg01'),
								  (N'VTChM03',N'Mobile Developer',N'ChNg01'),---
								  (N'VTChM04',N'AI Engineer',N'ChNg02'),
								  (N'VTChM05',N'AI Researcher',N'ChNg02'),---
								  (N'VTChM06',N'Data Analyst',N'ChNg03'),
								  (N'VTChM07',N'Data Engineer',N'ChNg03'),---
								  (N'VTChM08',N'Theo dõi đơn hàng',N'ChNg04'),
								  (N'VTChM09',N'Quản lý hệ thống vận tải',N'ChNg04'),---
								  (N'VTChM10',N'Tài xế xe tải',N'ChNg05'),
								  (N'VTChM11',N'Bốc xếp hàng hóa',N'ChNg05'),---
								  (N'VTChM12',N'Giáo viên tiểu học',N'ChNg06'),
								  (N'VTChM13',N'Giáo viên tiếng Anh',N'ChNg06'),---
								  (N'VTChM14',N'Huấn luyện viên Thể hình (PT)',N'ChNg07'),
								  (N'VTChM15',N'Huấn luyện viên Yoga',N'ChNg07'),---
								  (N'VTChM16',N'Thợ cơ khí',N'ChNg08'),
								  (N'VTChM17',N'Thợ hàn',N'ChNg08'),---
								  (N'VTChM18',N'Kỹ sư lập trình máy',N'ChNg09'),
								  (N'VTChM19',N'Kỹ sư vật liệu',N'ChNg09'),---
								  (N'VTChM20',N'Thợ điện',N'ChNg10'),
								  (N'VTChM21',N'Kỹ sư tự động hóa',N'ChNg10'),---
								  (N'VTChM22',N'Thiết kế vi mạch',N'ChNg11'),
								  (N'VTChM23',N'Lập trình nhúng',N'ChNg11')---
GO
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
INSERT INTO TrinhDo VALUES (N'TrD01',N'Sơ cấp'),
						   (N'TrD02',N'Trung cấp'),
						   (N'TrD03',N'Cao đẳng'),
						   (N'TrD04',N'Đại học'),
						   (N'TrD05',N'Thạc sĩ/Tiến sĩ')
GO

INSERT INTO CapBac VALUES (N'CaB01',N'Intern'),
						  (N'CaB02',N'Fresher'),
						  (N'CaB03',N'Junior'),
						  (N'CaB04',N'Senior')
GO

INSERT INTO CapBac VALUES (N'CaB05',N'Nhân viên')
GO

INSERT INTO KyNang VALUES (N'KN01',N'Microsoft 365'),
						  (N'KN02',N'Amazon Web Services (AWS)'),
						  (N'KN03',N'Adobe'),
						  (N'KN04',N'Google Cloud Platform'),
						  (N'KN05',N'Java'),
						  (N'KN06',N'C#'),
						  (N'KN07',N'.NET'),
						  (N'KN08',N'Python'),
						  (N'KN09',N'SQL'),
						  (N'KN10',N'React'),
						  (N'KN11',N'Mobile'),
						  (N'KN12',N'REST APIs'),
						  (N'KN13',N'Javascript'),
						  (N'KN14',N'Git'),
						  (N'KN15',N'C/C++'),
						  (N'KN16',N'Android Studio')

GO

INSERT INTO KyNangMem VALUES (N'KNM01',N'Giao tiếp tốt'),
							 (N'KNM02',N'Kỹ năng làm việc nhóm'),
							 (N'KNM03',N'Chịu được áp lực tốt'),
							 (N'KNM04',N'Kỹ năng thuyết trình'),
							 (N'KNM05',N'Tư duy logic'),
							 (N'KNM06',N'Nghiên cứu'),
							 (N'KNM07',N'Khả năng tự học'),
							 (N'KNM08',N'Giao tiếp tiếng Anh'),
							 (N'KNM09',N'Giao tiếp tiếng Nhật'),
							 (N'KNM10',N'Có kiến thức về công nghệ'),
							 (N'KNM11',N'Có chơi thể thao')
GO

INSERT INTO ChuyenMon VALUES (N'CM01',N'Công nghệ Thông tin'),
							 (N'CM02',N'Logistics'),--
							 (N'CM03',N'Giáo dục/Đào tạo'),--
							 (N'CM04',N'Sản xuất'),--
							 (N'CM05',N'Điện/Điện tử')
GO

INSERT INTO NgoaiNgu VALUES (N'NN01',N'Tiếng Anh'),
							(N'NN02',N'Tiếng Nhật'),
							(N'NN03',N'Tiếng Trung'),
							(N'NN04',N'Tiếng Pháp')
GO

-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
INSERT INTO CongTy VALUES (N'CoTy01',N'Công ty A',N'0123456789',N'215 ĐBP',N'congtya@gmail.com',N'111123'),
						  (N'CoTy02',N'Công ty B',N'0123456789',N'215 ĐBP',N'congtyb@gmail.com',N'111124'),
						  (N'CoTy03',N'Công ty C',N'0123456789',N'215 ĐBP',N'congtyc@gmail.com',N'111125'),
						  (N'CoTy04',N'Công ty D',N'0123456789',N'215 ĐBP',N'congtyd@gmail.com',N'111126'),
						  (N'CoTy05',N'Công ty E',N'0123456789',N'215 ĐBP',N'congtye@gmail.com',N'111127')
GO

INSERT INTO NhaTuyenDung VALUES (N'NTD01',N'Nguyễn Văn A',N'Nam',N'0123456789',N'213 ĐBP',N'ntda@gmail.com',N'CoTy01'),
								(N'NTD02',N'Nguyễn Văn B',N'Nam',N'0123456789',N'213 ĐBP',N'ntdb@gmail.com',N'CoTy02'),
								(N'NTD03',N'Nguyễn Văn C',N'Nam',N'0123456789',N'213 ĐBP',N'ntdc@gmail.com',N'CoTy03'),
								(N'NTD04',N'Nguyễn Văn D',N'Nam',N'0123456789',N'213 ĐBP',N'ntdd@gmail.com',N'CoTy04'),
								(N'NTD05',N'Nguyễn Văn E',N'Nam',N'0123456789',N'213 ĐBP',N'ntde@gmail.com',N'CoTy05')
GO

INSERT INTO UngVien VALUES (N'UV01',N'Nguyễn Thanh A',N'Nam',N'0123456789',N'PX06',N'uva@gmail.com'),
						   (N'UV02',N'Nguyễn Thanh B',N'Nam',N'0123456789',N'PX02',N'uvb@gmail.com'),
						   (N'UV03',N'Nguyễn Thanh C',N'Nam',N'0123456789',N'PX03',N'uvc@gmail.com'),
						   (N'UV04',N'Nguyễn Thị D',N'Nữ',N'0123456789',N'PX07',N'uvd@gmail.com'),
						   (N'UV05',N'Nguyễn Thị E',N'Nữ',N'0123456789',N'PX15',N'uve@gmail.com')
GO

INSERT INTO CongViec VALUES (N'CV01',N'Intern Backend Dev',N'NTD01',N'VTChM01',N'PX01',6000000,N'CaB01',18,0,N'Nam',N'TrD04',N'CM01',N'NN01'),
							(N'CV02',N'Junior Backend Dev',N'NTD01',N'VTChM01',N'PX02',15000000,N'CaB03',18,2,N'Nam',N'TrD04',N'CM01',N'NN01'),
							(N'CV03',N'Senior Backend Dev',N'NTD01',N'VTChM01',N'PX03',25000000,N'CaB04',18,3,N'Nam',N'TrD04',N'CM01',N'NN02'),
							---
							(N'CV04',N'Intern Fullstack Dev',N'NTD01',N'VTChM02',N'PX01',7000000,N'CaB01',18,0,N'Nam',N'TrD04',N'CM01',N'NN01'),
							(N'CV05',N'Fresher Fullstack Dev',N'NTD01',N'VTChM02',N'PX02',12000000,N'CaB02',18,0,N'Nam',N'TrD04',N'CM01',N'NN01'),
							(N'CV06',N'Senior Fullstack Dev',N'NTD01',N'VTChM02',N'PX03',27000000,N'CaB04',18,3,N'Nam',N'TrD04',N'CM01',N'NN01'),
							---
							(N'CV07',N'Junior Mobile Dev',N'NTD01',N'VTChM03',N'PX05',18000000,N'CaB03',18,2,N'Nam',N'TrD04',N'CM01',N'NN01'),
							(N'CV08',N'Senior Mobile Dev',N'NTD01',N'VTChM03',N'PX04',28000000,N'CaB04',18,4,N'Nam',N'TrD04',N'CM01',N'NN02'),
							------
							(N'CV09',N'Intern AI Engineer',N'NTD01',N'VTChM04',N'PX06',8000000,N'CaB01',18,0,N'Nam',N'TrD04',N'CM01',N'NN01'),
							(N'CV10',N'Junior AI Engineer',N'NTD01',N'VTChM04',N'PX05',20000000,N'CaB03',18,2,N'Nam',N'TrD04',N'CM01',N'NN01'),
							(N'CV11',N'Senior AI Engineer',N'NTD01',N'VTChM04',N'PX05',27000000,N'CaB04',18,4,N'Nam',N'TrD04',N'CM01',N'NN01'),
							---
							(N'CV12',N'Junior AI Researcher',N'NTD01',N'VTChM05',N'PX01',18000000,N'CaB03',18,1,N'Nam',N'TrD04',N'CM01',N'NN01'),
							(N'CV13',N'Senior AI Researcher',N'NTD01',N'VTChM05',N'PX03',24000000,N'CaB04',18,3,N'Nam',N'TrD04',N'CM01',N'NN03'),
							------
							(N'CV14',N'Fresher Data Analyst',N'NTD01',N'VTChM06',N'PX01',12000000,N'CaB02',18,0,N'Nam',N'TrD04',N'CM01',N'NN02'),
							(N'CV15',N'Junior Data Analyst',N'NTD01',N'VTChM06',N'PX02',14000000,N'CaB03',18,1,N'Nam',N'TrD04',N'CM01',N'NN02'),
							(N'CV16',N'Senior Data Analyst',N'NTD01',N'VTChM06',N'PX03',24000000,N'CaB04',18,3,N'Nam',N'TrD04',N'CM01',N'NN02'),
							---
							(N'CV17',N'Junior Data Engineer',N'NTD01',N'VTChM07',N'PX06',18000000,N'CaB03',18,1,N'Nam',N'TrD04',N'CM01',N'NN01'),
							(N'CV18',N'Senior Data Engineer',N'NTD01',N'VTChM07',N'PX07',24000000,N'CaB04',18,3,N'Nam',N'TrD04',N'CM01',N'NN03'),
							------
							(N'CV19',N'Nhân viên Theo dõi đơn hàng',N'NTD02',N'VTChM08',N'PX14',15000000,N'CaB02',18,1,N'Nữ',N'TrD04',N'CM02',N'NN01'),
							(N'CV20',N'Nhân viên Theo dõi đơn hàng',N'NTD02',N'VTChM08',N'PX15',20000000,N'CaB03',18,2,N'Nam',N'TrD04',N'CM02',N'NN03'),
							---
							(N'CV21',N'Nhân viên Phòng quản lý xe',N'NTD02',N'VTChM09',N'PX14',22000000,N'CaB02',18,1,N'Nữ',N'TrD04',N'CM02',N'NN01'),
							(N'CV22',N'Nhân viên Quản lý Mạng lưới tổng hợp',N'NTD02',N'VTChM09',N'PX15',24000000,N'CaB03',18,2,N'Nam',N'TrD04',N'CM02',N'NN02'),
							------
							(N'CV23',N'Nhân viên Lái Xe tải',N'NTD02',N'VTChM10',N'PX16',28000000,N'CaB03',18,2,N'Nam',N'TrD04',N'CM02',N'NN01'),
							(N'CV24',N'Tài xế xe Container',N'NTD02',N'VTChM10',N'PX15',30000000,N'CaB03',18,2,N'Nam',N'TrD04',N'CM02',N'NN01'),
							---
							(N'CV25',N'Nhân viên Bốc xếp hàng hóa',N'NTD02',N'VTChM11',N'PX14',15000000,N'CaB02',18,1,N'Nam',N'TrD04',N'CM02',N'NN01'),
							(N'CV26',N'Nhân viên Trực kho',N'NTD02',N'VTChM11',N'PX15',20000000,N'CaB03',18,2,N'Nam',N'TrD04',N'CM02',N'NN03'),
							------
							(N'CV27',N'Giáo viên trường tiểu học A',N'NTD03',N'VTChM12',N'PX08',20000000,N'CaB03',18,1,N'Nữ',N'TrD04',N'CM03',N'NN01'),
							(N'CV28',N'Giáo viên trường tiểu học B',N'NTD03',N'VTChM12',N'PX09',22000000,N'CaB03',18,2,N'Nữ',N'TrD04',N'CM03',N'NN01'),
							---
							(N'CV29',N'Giáo viên tiếng Anh A',N'NTD03',N'VTChM13',N'PX08',22000000,N'CaB03',18,2,N'Nữ',N'TrD04',N'CM03',N'NN01'),
							(N'CV30',N'Giáo viên tiếng Anh B',N'NTD03',N'VTChM13',N'PX09',24000000,N'CaB03',18,2,N'Nam',N'TrD04',N'CM03',N'NN01'),
							------
							(N'CV31',N'PT Freelancer',N'NTD03',N'VTChM14',N'PX08',20000000,N'CaB03',18,1,N'Nam',N'TrD04',N'CM03',N'NN01'),
							------
							(N'CV32',N'Huấn luyện viên Yoga',N'NTD03',N'VTChM15',N'PX12',22000000,N'CaB03',18,2,N'Nữ',N'TrD04',N'CM03',N'NN01'),
							------
							(N'CV33',N'Nhân viên cơ khí xưởng',N'NTD04',N'VTChM16',N'PX03',20000000,N'CaB03',18,1,N'Nam',N'TrD04',N'CM04',N'NN01'),
							------
							(N'CV34',N'Nhân viên kỹ thuật',N'NTD04',N'VTChM17',N'PX09',17000000,N'CaB03',18,0,N'Nam',N'TrD04',N'CM04',N'NN01'),
							------
							(N'CV35',N'Nhân viên Lập trình và Vận hành',N'NTD04',N'VTChM18',N'PX16',22000000,N'CaB03',18,2,N'Nam',N'TrD04',N'CM04',N'NN01'),
							------
							(N'CV36',N'Kỹ sư Công nghệ Vật liệu',N'NTD04',N'VTChM19',N'PX09',20000000,N'CaB03',18,2,N'Nam',N'TrD04',N'CM04',N'NN01'),
							------
							(N'CV37',N'Nhân viên Kỹ thuật Điện',N'NTD04',N'VTChM20',N'PX04',17000000,N'CaB03',18,1,N'Nam',N'TrD04',N'CM05',N'NN01'),
							------
							(N'CV38',N'Kỹ thuật viên Điện Tự động hóa',N'NTD04',N'VTChM21',N'PX05',22000000,N'CaB03',18,2,N'Nam',N'TrD04',N'CM05',N'NN01'),
							------
							(N'CV39',N'Kỹ sư thiết kế vi mạch IC',N'NTD04',N'VTChM22',N'PX07',28000000,N'CaB03',18,2,N'Nam',N'TrD04',N'CM05',N'NN01'),
							------
							(N'CV40',N'Kỹ sư Lập trình nhúng',N'NTD04',N'VTChM23',N'PX10',18000000,N'CaB03',18,1,N'Nam',N'TrD04',N'CM05',N'NN01')
GO

                   
INSERT INTO ChiTietKyNang VALUES (N'CV01',N'KN05'),
								 (N'CV01',N'KN09'),
								 (N'CV02',N'KN06'),
								 (N'CV02',N'KN07'),
								 (N'CV03',N'KN08'),
								 (N'CV03',N'KN09'),
								 (N'CV03',N'KN14'),
								 (N'CV04',N'KN05'),
								 (N'CV04',N'KN09'),
								 (N'CV05',N'KN08'),
								 (N'CV05',N'KN12'),
								 (N'CV06',N'KN08'),
								 (N'CV06',N'KN12'),
								 (N'CV06',N'KN14'),

								 (N'CV07',N'KN05'),
								 (N'CV07',N'KN16'),

								 (N'CV08',N'KN05'),
								 (N'CV08',N'KN16'),
								 (N'CV08',N'KN14'),

								 (N'CV09',N'KN08'),
								 (N'CV09',N'KN12'),

								 (N'CV10',N'KN08'),
								 (N'CV10',N'KN12'),
								 (N'CV10',N'KN09'),

								 (N'CV11',N'KN08'),
								 (N'CV11',N'KN12'),
								 (N'CV11',N'KN14'),

								 (N'CV12',N'KN08'),
								 (N'CV13',N'KN08'),

								 (N'CV14',N'KN01'),
								 (N'CV14',N'KN08'),

								 (N'CV15',N'KN01'),
								 (N'CV15',N'KN08'),
								 (N'CV15',N'KN09'),

								 (N'CV16',N'KN01'),
								 (N'CV16',N'KN08'),
								 (N'CV16',N'KN09'),

								 (N'CV17',N'KN08'),
								 (N'CV17',N'KN09'),
								 (N'CV17',N'KN04'),

								 (N'CV18',N'KN08'),
								 (N'CV18',N'KN09'),
								 (N'CV18',N'KN04'),
								 (N'CV19',N'KN01'),
								 (N'CV20',N'KN01'),
								 (N'CV21',N'KN01'),
								 (N'CV22',N'KN01'),
								 (N'CV23',N'KN01'),
								 (N'CV24',N'KN01'),
								 (N'CV25',N'KN01'),
								 (N'CV26',N'KN01'),
								 (N'CV27',N'KN01'),
								 (N'CV28',N'KN01'),
								 (N'CV29',N'KN01'),
								 (N'CV30',N'KN01'),
								 (N'CV31',N'KN01'),
								 (N'CV32',N'KN01'),
								 (N'CV33',N'KN01'),
								 (N'CV34',N'KN01'),
								 (N'CV35',N'KN01'),
								 (N'CV36',N'KN01'),
								 (N'CV37',N'KN01'),
								 (N'CV38',N'KN01'),
								 (N'CV39',N'KN01'),
								 (N'CV40',N'KN01')
GO

INSERT INTO ChiTietKyNangMem VALUES (N'CV01',N'KNM01'),
									(N'CV01',N'KNM02'),
									(N'CV02',N'KNM01'),
									(N'CV03',N'KNM01'),
									(N'CV04',N'KNM01'),
									(N'CV05',N'KNM01'),
									(N'CV06',N'KNM01'),
									(N'CV07',N'KNM01'),
									(N'CV08',N'KNM01'),
									(N'CV09',N'KNM01'),
									(N'CV10',N'KNM01'),
									(N'CV11',N'KNM01'),
									(N'CV12',N'KNM01'),
									(N'CV13',N'KNM01'),
									(N'CV14',N'KNM01'),
									(N'CV15',N'KNM01'),
									(N'CV16',N'KNM01'),
									(N'CV17',N'KNM01'),
									(N'CV18',N'KNM01'),
									(N'CV19',N'KNM01'),
									(N'CV20',N'KNM01'),
									(N'CV21',N'KNM01'),
									(N'CV22',N'KNM01'),
									(N'CV23',N'KNM01'),
									(N'CV24',N'KNM01'),
									(N'CV25',N'KNM01'),
									(N'CV26',N'KNM01'),
									(N'CV27',N'KNM01'),
									(N'CV28',N'KNM01'),
									(N'CV29',N'KNM01'),
									(N'CV30',N'KNM01'),
									(N'CV31',N'KNM01'),
									(N'CV32',N'KNM01'),
									(N'CV33',N'KNM01'),
									(N'CV34',N'KNM01'),
									(N'CV35',N'KNM01'),
									(N'CV36',N'KNM01'),
									(N'CV37',N'KNM01'),
									(N'CV38',N'KNM01'),
									(N'CV39',N'KNM01'),
									(N'CV40',N'KNM01')
GO


--
--Query ALL CongViec + Filter
DECLARE @ViTri NVARCHAR(100) = N'';  
DECLARE @ChuyenNganh NVARCHAR(100) = N'';  
DECLARE @NganhNghe NVARCHAR(100) = N'';  
DECLARE @PhuongXa NVARCHAR(100) = N'';  
DECLARE @QuanHuyen NVARCHAR(100) = N'';  
DECLARE @TinhTP NVARCHAR(100) = N'';  
DECLARE @CapBac NVARCHAR(100) = N'';  
DECLARE @TrinhDo NVARCHAR(100) = N'';  
DECLARE @ChuyenMon NVARCHAR(100) = N'';  
DECLARE @NgoaiNgu NVARCHAR(100) = N'';  
DECLARE @KyNang NVARCHAR(100) = N'';  
DECLARE @KyNangMem NVARCHAR(100) = N'';  
DECLARE @MucLuongMin INT = 10000000; -- Lương tối thiểu
DECLARE @MucLuongMax INT = NULL; -- Lương tối đa
DECLARE @DoTuoiMin INT = NULL; -- Độ tuổi tối thiểu
DECLARE @DoTuoiMax INT = NULL; -- Độ tuổi tối đa


WITH KyNang_CTE AS (
    SELECT 
        CV.Id_CongViec,
        STRING_AGG(KN.Ten_KyNang, ', ') AS DanhSachKyNang
    FROM CongViec CV
    LEFT JOIN ChiTietKyNang CTK ON CV.Id_CongViec = CTK.Id_CongViec
    LEFT JOIN KyNang KN ON CTK.Id_KyNang = KN.Id_KyNang
    GROUP BY CV.Id_CongViec
),
KyNangMem_CTE AS (
    SELECT 
        CV.Id_CongViec,
        STRING_AGG(KNM.Ten_KyNangMem, ', ') AS DanhSachKyNangMem
    FROM CongViec CV
    LEFT JOIN ChiTietKyNangMem CTKM ON CV.Id_CongViec = CTKM.Id_CongViec
    LEFT JOIN KyNangMem KNM ON CTKM.Id_KyNangMem = KNM.Id_KyNangMem
    GROUP BY CV.Id_CongViec
)
SELECT 
    CV.Id_CongViec, 
    CV.Ten_CongViec, 
    NTD.Ten_NhaTuyenDung,
    VT.Ten_ViTri, 
    CN.Ten_ChuyenNganh,
    NGN.Ten_NganhNghe, 
    PX.Ten_PhuongXa, 
    QH.Ten_QuanHuyen, 
    TTP.Ten_TinhTP, 
    CB.Ten_CapBac, 
    TD.Ten_TrinhDo, 
    CM.Ten_ChuyenMon, 
    NN.Ten_NgoaiNgu,
    CV.MucLuong_CongViec,
    CV.DoTuoi_CongViec,
    COALESCE(KNCTE.DanhSachKyNang, '') AS DanhSachKyNang,
    COALESCE(KNMCTE.DanhSachKyNangMem, '') AS DanhSachKyNangMem
FROM CongViec CV 
INNER JOIN NhaTuyenDung NTD ON CV.Id_NhaTuyenDung = NTD.Id_NhaTuyenDung
INNER JOIN ViTriChuyenMon VT ON CV.ViTri_CongViec = VT.Id_ViTri 
INNER JOIN ChuyenNganh CN ON VT.Id_ChuyenNganh = CN.Id_ChuyenNganh 
INNER JOIN NganhNghe NGN ON CN.Id_NganhNghe = NGN.Id_NganhNghe
INNER JOIN PhuongXa PX ON CV.KhuVuc_CongViec = PX.Id_PhuongXa 
INNER JOIN QuanHuyen QH ON PX.Id_QuanHuyen = QH.Id_QuanHuyen 
INNER JOIN TinhTP TTP ON QH.Id_TinhTP = TTP.Id_TinhTP
INNER JOIN CapBac CB ON CV.CapBac_CongViec = CB.Id_CapBac
INNER JOIN TrinhDo TD ON CV.TrinhDo_CongViec = TD.Id_TrinhDo
INNER JOIN ChuyenMon CM ON CV.ChuyenMon_CongViec = CM.Id_ChuyenMon
INNER JOIN NgoaiNgu NN ON CV.NgoaiNgu_CongViec = NN.Id_NgoaiNgu
LEFT JOIN KyNang_CTE KNCTE ON CV.Id_CongViec = KNCTE.Id_CongViec
LEFT JOIN KyNangMem_CTE KNMCTE ON CV.Id_CongViec = KNMCTE.Id_CongViec
WHERE 
    (@NganhNghe = '' OR NGN.Ten_NganhNghe IN (SELECT value FROM STRING_SPLIT(@NganhNghe, ','))) 
    AND (@ChuyenNganh = '' OR CN.Ten_ChuyenNganh IN (SELECT value FROM STRING_SPLIT(@ChuyenNganh, ','))) 
    AND (@ViTri = '' OR VT.Ten_ViTri IN (SELECT value FROM STRING_SPLIT(@ViTri, ','))) 
    AND (@TinhTP = '' OR TTP.Ten_TinhTP IN (SELECT value FROM STRING_SPLIT(@TinhTP, ','))) 
    AND (@QuanHuyen = '' OR QH.Ten_QuanHuyen IN (SELECT value FROM STRING_SPLIT(@QuanHuyen, ','))) 
    AND (@PhuongXa = '' OR PX.Ten_PhuongXa IN (SELECT value FROM STRING_SPLIT(@PhuongXa, ','))) 
    AND (@CapBac = '' OR CB.Ten_CapBac IN (SELECT value FROM STRING_SPLIT(@CapBac, ','))) 
    AND (@TrinhDo = '' OR TD.Ten_TrinhDo IN (SELECT value FROM STRING_SPLIT(@TrinhDo, ','))) 
    AND (@ChuyenMon = '' OR CM.Ten_ChuyenMon IN (SELECT value FROM STRING_SPLIT(@ChuyenMon, ','))) 
    AND (@NgoaiNgu = '' OR NN.Ten_NgoaiNgu IN (SELECT value FROM STRING_SPLIT(@NgoaiNgu, ','))) 
    -- Lọc theo mức lương min - max
    AND (@MucLuongMin IS NULL OR CV.MucLuong_CongViec >= @MucLuongMin)
    AND (@MucLuongMax IS NULL OR CV.MucLuong_CongViec <= @MucLuongMax)
    -- Lọc theo độ tuổi min - max
    AND (@DoTuoiMin IS NULL OR CV.DoTuoi_CongViec >= @DoTuoiMin)
    AND (@DoTuoiMax IS NULL OR CV.DoTuoi_CongViec <= @DoTuoiMax)
    -- Lọc theo kỹ năng
    AND (@KyNang = '' OR EXISTS (
        SELECT 1 FROM ChiTietKyNang CTK
        JOIN KyNang KN ON CTK.Id_KyNang = KN.Id_KyNang
        WHERE CTK.Id_CongViec = CV.Id_CongViec
        AND KN.Ten_KyNang IN (SELECT value FROM STRING_SPLIT(@KyNang, ','))
    )) 
    -- Lọc theo kỹ năng mềm
    AND (@KyNangMem = '' OR EXISTS (
        SELECT 1 FROM ChiTietKyNangMem CTKM
        JOIN KyNangMem KNM ON CTKM.Id_KyNangMem = KNM.Id_KyNangMem
        WHERE CTKM.Id_CongViec = CV.Id_CongViec
        AND KNM.Ten_KyNangMem IN (SELECT value FROM STRING_SPLIT(@KyNangMem, ','))
    )); 

-- UPDATE
DECLARE @ViTri NVARCHAR(100) = N'Backend Developer'; 
DECLARE @ChuyenNganh NVARCHAR(100) = N''; 
DECLARE @NganhNghe NVARCHAR(100) = N''; 
DECLARE @PhuongXa NVARCHAR(100) = N''; 
DECLARE @QuanHuyen NVARCHAR(100) = N''; 
DECLARE @TinhTP NVARCHAR(100) = N''; 
DECLARE @CapBac NVARCHAR(100) = N''; 
DECLARE @TrinhDo NVARCHAR(100) = N''; 
DECLARE @ChuyenMon NVARCHAR(100) = N''; 
DECLARE @NgoaiNgu NVARCHAR(100) = N''; 
DECLARE @KyNang NVARCHAR(MAX) = N''; 
DECLARE @KyNangMem NVARCHAR(MAX) = N''; 
DECLARE @MucLuongMin INT = null; 
DECLARE @MucLuongMax INT = null; 
DECLARE @DoTuoiMin INT = null; 
DECLARE @DoTuoiMax INT = null; 
DECLARE @GioiTinh NVARCHAR(10) = N''; 
DECLARE @KinhNghiem INT = null; 

            -- CTE 1: Lấy danh sách kỹ năng
            WITH KyNang_CTE AS (
                SELECT 
                    CV.Id_CongViec,
                    STRING_AGG(KN.Ten_KyNang, ', ') AS DanhSachKyNang
                FROM CongViec CV
                LEFT JOIN ChiTietKyNang CTK ON CV.Id_CongViec = CTK.Id_CongViec
                LEFT JOIN KyNang KN ON CTK.Id_KyNang = KN.Id_KyNang
                GROUP BY CV.Id_CongViec
            ),
            KyNangMem_CTE AS (
                SELECT 
                    CV.Id_CongViec,
                    STRING_AGG(KNM.Ten_KyNangMem, ', ') AS DanhSachKyNangMem
                FROM CongViec CV
                LEFT JOIN ChiTietKyNangMem CTKM ON CV.Id_CongViec = CTKM.Id_CongViec
                LEFT JOIN KyNangMem KNM ON CTKM.Id_KyNangMem = KNM.Id_KyNangMem
                GROUP BY CV.Id_CongViec
            ),
            -- CTE 2: Tính số kỹ năng khớp
            MatchScore_CTE AS (
                SELECT 
                    CV.Id_CongViec,
                    COUNT(DISTINCT KN.Ten_KyNang) AS MatchKyNang
                FROM CongViec CV
                LEFT JOIN ChiTietKyNang CTK ON CV.Id_CongViec = CTK.Id_CongViec
                LEFT JOIN KyNang KN ON CTK.Id_KyNang = KN.Id_KyNang
                WHERE KN.Ten_KyNang IN (SELECT value FROM STRING_SPLIT(@KyNang, ','))
                GROUP BY CV.Id_CongViec
            ),
            MatchScoreMem_CTE AS (
                SELECT 
                    CV.Id_CongViec,
                    COUNT(DISTINCT KNM.Ten_KyNangMem) AS MatchKyNangMem
                FROM CongViec CV
                LEFT JOIN ChiTietKyNangMem CTKM ON CV.Id_CongViec = CTKM.Id_CongViec
                LEFT JOIN KyNangMem KNM ON CTKM.Id_KyNangMem = KNM.Id_KyNangMem
                WHERE KNM.Ten_KyNangMem IN (SELECT value FROM STRING_SPLIT(@KyNangMem, ','))
                GROUP BY CV.Id_CongViec
            )
            SELECT 
                CV.Id_CongViec, 
                CV.Ten_CongViec, 
                NTD.Ten_NhaTuyenDung, 
                VT.Ten_ViTri,
                CN.Ten_ChuyenNganh, 
                NGN.Ten_NganhNghe, 
                PX.Ten_PhuongXa, 
                QH.Ten_QuanHuyen, 
                TTP.Ten_TinhTP, 
                CB.Ten_CapBac, 
                TD.Ten_TrinhDo, 
                CM.Ten_ChuyenMon, 
                NN.Ten_NgoaiNgu,
                CV.MucLuong_CongViec,
                CV.DoTuoi_CongViec,
                CV.KinhNghiem_CongViec,
                CV.GioiTinh_CongViec,
                COALESCE(KNCTE.DanhSachKyNang, '') AS DanhSachKyNang,
                COALESCE(KNMCTE.DanhSachKyNangMem, '') AS DanhSachKyNangMem,
                COALESCE(MSC.MatchKyNang, 0) + COALESCE(MSM.MatchKyNangMem, 0) AS MatchScore -- Tổng điểm khớp kỹ năng
            FROM CongViec CV 
            INNER JOIN NhaTuyenDung NTD ON CV.Id_NhaTuyenDung = NTD.Id_NhaTuyenDung
            INNER JOIN ViTriChuyenMon VT ON CV.ViTri_CongViec = VT.Id_ViTri 
            INNER JOIN ChuyenNganh CN ON VT.Id_ChuyenNganh = CN.Id_ChuyenNganh 
            INNER JOIN NganhNghe NGN ON CN.Id_NganhNghe = NGN.Id_NganhNghe
            INNER JOIN PhuongXa PX ON CV.KhuVuc_CongViec = PX.Id_PhuongXa 
            INNER JOIN QuanHuyen QH ON PX.Id_QuanHuyen = QH.Id_QuanHuyen 
            INNER JOIN TinhTP TTP ON QH.Id_TinhTP = TTP.Id_TinhTP
            INNER JOIN CapBac CB ON CV.CapBac_CongViec = CB.Id_CapBac
            INNER JOIN TrinhDo TD ON CV.TrinhDo_CongViec = TD.Id_TrinhDo
            INNER JOIN ChuyenMon CM ON CV.ChuyenMon_CongViec = CM.Id_ChuyenMon
            INNER JOIN NgoaiNgu NN ON CV.NgoaiNgu_CongViec = NN.Id_NgoaiNgu
            LEFT JOIN KyNang_CTE KNCTE ON CV.Id_CongViec = KNCTE.Id_CongViec
            LEFT JOIN KyNangMem_CTE KNMCTE ON CV.Id_CongViec = KNMCTE.Id_CongViec
            LEFT JOIN MatchScore_CTE MSC ON CV.Id_CongViec = MSC.Id_CongViec
            LEFT JOIN MatchScoreMem_CTE MSM ON CV.Id_CongViec = MSM.Id_CongViec
            WHERE 
                (@NganhNghe = '' OR NGN.Ten_NganhNghe IN (SELECT value FROM STRING_SPLIT(@NganhNghe, ','))) 
                AND (@ChuyenNganh = '' OR CN.Ten_ChuyenNganh IN (SELECT value FROM STRING_SPLIT(@ChuyenNganh, ','))) 
                AND (@ViTri = '' OR VT.Ten_ViTri IN (SELECT value FROM STRING_SPLIT(@ViTri, ','))) 
                AND (@TinhTP = '' OR TTP.Ten_TinhTP IN (SELECT value FROM STRING_SPLIT(@TinhTP, ','))) 
                AND (@QuanHuyen = '' OR QH.Ten_QuanHuyen IN (SELECT value FROM STRING_SPLIT(@QuanHuyen, ','))) 
                AND (@PhuongXa = '' OR PX.Ten_PhuongXa IN (SELECT value FROM STRING_SPLIT(@PhuongXa, ','))) 
                AND (@CapBac = '' OR CB.Ten_CapBac IN (SELECT value FROM STRING_SPLIT(@CapBac, ','))) 
                AND (@TrinhDo = '' OR TD.Ten_TrinhDo IN (SELECT value FROM STRING_SPLIT(@TrinhDo, ','))) 
                AND (@ChuyenMon = '' OR CM.Ten_ChuyenMon IN (SELECT value FROM STRING_SPLIT(@ChuyenMon, ','))) 
                AND (@NgoaiNgu = '' OR NN.Ten_NgoaiNgu IN (SELECT value FROM STRING_SPLIT(@NgoaiNgu, ','))) 
                AND (@GioiTinh = '' OR CV.GioiTinh_CongViec = @GioiTinh)
                AND (@KinhNghiem IS NULL OR CV.KinhNghiem_CongViec >= @KinhNghiem)
                AND (@MucLuongMin IS NULL OR CV.MucLuong_CongViec >= @MucLuongMin)
                AND (@MucLuongMax IS NULL OR CV.MucLuong_CongViec <= @MucLuongMax)
                AND (@DoTuoiMin IS NULL OR CV.DoTuoi_CongViec >= @DoTuoiMin)
                AND (@DoTuoiMax IS NULL OR CV.DoTuoi_CongViec <= @DoTuoiMax)
            ORDER BY MatchScore DESC, Id_CongViec ASC;
--


SELECT *
FROM CongViec

	SELECT TOP 3 *
	FROM FilterUV
	WHERE Id_UngVien = 'UV01'
	ORDER BY ThoiGian DESC


INSERT INTO FilterUV 
VALUES 
-- Dòng 1: ngày hôm qua
(N'UV01', DATEADD(DAY, -2, GETDATE()), N'Backend Developer', N'Software Engineering', N'Công nghệ Thông tin', NULL, NULL, N'Hồ Chí Minh', N'Junior', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, N'Java', NULL),

-- Dòng 2: hôm nay (GETDATE)
(N'UV01', DATEADD(DAY, -1, GETDATE()), N'Fullstack Developer', N'Software Engineering', N'Công nghệ Thông tin', NULL, N'Quận Bình Thạnh', N'Hồ Chí Minh', N'Junior', NULL, NULL, NULL, 10000000, NULL, NULL, NULL, 1, NULL, N'Java', NULL)

INSERT INTO FilterUV 
VALUES 
-- Dòng 1: ngày hôm qua
(N'UV02', DATEADD(DAY, -2, GETDATE()), N'AI Engineer', N'Artificial Intelligent (AI)', N'Công nghệ Thông tin', NULL, NULL, N'Hồ Chí Minh', N'Senior', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, N'Python', NULL),

-- Dòng 2: hôm nay (GETDATE)
(N'UV02', DATEADD(DAY, -1, GETDATE()), N'AI Researcher', N'Artificial Intelligent (AI)', N'Công nghệ Thông tin', NULL, NULL, N'Hồ Chí Minh', N'Senior', NULL, NULL, NULL, 20000000, NULL, NULL, NULL, 1, NULL, N'Python', NULL)

INSERT INTO FilterUV 
VALUES 
-- Dòng 1: ngày hôm qua
(N'UV03', DATEADD(DAY, -2, GETDATE()), N'Giáo viên tiểu học', N'Giáo viên', N'Giáo dục/Đào tạo', NULL, NULL, N'Hồ Chí Minh', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),





INSERT INTO FilterUV (
    Id_UngVien, ThoiGian,
    ViTri, ChuyenNganh, NganhNghe,
    PhuongXa, QuanHuyen, TinhTP,
    CapBac, TrinhDo, ChuyenMon, NgoaiNgu,
    KyNang, KyNangMem,
    ThuNhapMin, ThuNhapMax,
    TuoiMin, TuoiMax,
    KinhNghiem, GioiTinh
)
VALUES (
    N'UV01', GETDATE(),
    N'Backend Developer', N'Software Engineering', N'Công nghệ Thông tin',
    N'Phường 6', N'Quận Bình Thạnh', N'Hồ Chí Minh',
    N'Intern', N'Đại học', N'Công nghệ Thông tin', N'Tiếng Anh',
    N'Java, SQL', N'Giao tiếp tốt, Kỹ năng làm việc nhóm',
    5000000, 10000000,
    20, 25,
    0, 'Nam'
);


SELECT 
                CV.Id_CongViec, CV.Ten_CongViec, 
                VT.Ten_ViTri, CB.Ten_CapBac, TD.Ten_TrinhDo, 
                CM.Ten_ChuyenMon, NN.Ten_NgoaiNgu,
                ISNULL(KN.DanhSachKyNang, '') AS KyNang,
                ISNULL(KNM.DanhSachKyNangMem, '') AS KyNangMem,
                QH.Ten_QuanHuyen, TTP.Ten_TinhTP
            FROM CongViec CV
            JOIN ViTriChuyenMon VT ON CV.ViTri_CongViec = VT.Id_ViTri
            JOIN CapBac CB ON CV.CapBac_CongViec = CB.Id_CapBac
            JOIN TrinhDo TD ON CV.TrinhDo_CongViec = TD.Id_TrinhDo
            JOIN ChuyenMon CM ON CV.ChuyenMon_CongViec = CM.Id_ChuyenMon
            JOIN NgoaiNgu NN ON CV.NgoaiNgu_CongViec = NN.Id_NgoaiNgu
            JOIN PhuongXa PX ON CV.KhuVuc_CongViec = PX.Id_PhuongXa
            JOIN QuanHuyen QH ON PX.Id_QuanHuyen = QH.Id_QuanHuyen
            JOIN TinhTP TTP ON QH.Id_TinhTP = TTP.Id_TinhTP
            LEFT JOIN (
                SELECT Id_CongViec, STRING_AGG(Ten_KyNang, ', ') AS DanhSachKyNang
                FROM ChiTietKyNang CTK JOIN KyNang KN ON CTK.Id_KyNang = KN.Id_KyNang
                GROUP BY Id_CongViec
            ) AS KN ON CV.Id_CongViec = KN.Id_CongViec
            LEFT JOIN (
                SELECT Id_CongViec, STRING_AGG(Ten_KyNangMem, ', ') AS DanhSachKyNangMem
                FROM ChiTietKyNangMem CTKM JOIN KyNangMem KNM ON CTKM.Id_KyNangMem = KNM.Id_KyNangMem
                GROUP BY Id_CongViec
            ) AS KNM ON CV.Id_CongViec = KNM.Id_CongViec





-----------------------------------
WITH KyNang_CTE AS (
                SELECT 
                    CV.Id_CongViec,
                    STRING_AGG(KN.Ten_KyNang, ', ') AS DanhSachKyNang
                FROM CongViec CV
                LEFT JOIN ChiTietKyNang CTK ON CV.Id_CongViec = CTK.Id_CongViec
                LEFT JOIN KyNang KN ON CTK.Id_KyNang = KN.Id_KyNang
                GROUP BY CV.Id_CongViec
            ),
            KyNangMem_CTE AS (
                SELECT 
                    CV.Id_CongViec,
                    STRING_AGG(KNM.Ten_KyNangMem, ', ') AS DanhSachKyNangMem
                FROM CongViec CV
                LEFT JOIN ChiTietKyNangMem CTKM ON CV.Id_CongViec = CTKM.Id_CongViec
                LEFT JOIN KyNangMem KNM ON CTKM.Id_KyNangMem = KNM.Id_KyNangMem
                GROUP BY CV.Id_CongViec
            )
            SELECT 
                CV.Id_CongViec, 
                CV.Ten_CongViec, 
                NTD.Ten_NhaTuyenDung, 
                VT.Ten_ViTri,
                CN.Ten_ChuyenNganh, 
                NGN.Ten_NganhNghe, 
                PX.Ten_PhuongXa, 
                QH.Ten_QuanHuyen, 
                TTP.Ten_TinhTP, 
                CB.Ten_CapBac, 
                TD.Ten_TrinhDo, 
                CM.Ten_ChuyenMon, 
                NN.Ten_NgoaiNgu,
                CV.MucLuong_CongViec,
                CV.DoTuoi_CongViec,
                CV.KinhNghiem_CongViec,
                CV.GioiTinh_CongViec,
                COALESCE(KNCTE.DanhSachKyNang, '') AS DanhSachKyNang,
                COALESCE(KNMCTE.DanhSachKyNangMem, '') AS DanhSachKyNangMem
            FROM CongViec CV 
            INNER JOIN NhaTuyenDung NTD ON CV.Id_NhaTuyenDung = NTD.Id_NhaTuyenDung
            INNER JOIN ViTriChuyenMon VT ON CV.ViTri_CongViec = VT.Id_ViTri 
            INNER JOIN ChuyenNganh CN ON VT.Id_ChuyenNganh = CN.Id_ChuyenNganh 
            INNER JOIN NganhNghe NGN ON CN.Id_NganhNghe = NGN.Id_NganhNghe
            INNER JOIN PhuongXa PX ON CV.KhuVuc_CongViec = PX.Id_PhuongXa 
            INNER JOIN QuanHuyen QH ON PX.Id_QuanHuyen = QH.Id_QuanHuyen 
            INNER JOIN TinhTP TTP ON QH.Id_TinhTP = TTP.Id_TinhTP
            INNER JOIN CapBac CB ON CV.CapBac_CongViec = CB.Id_CapBac
            INNER JOIN TrinhDo TD ON CV.TrinhDo_CongViec = TD.Id_TrinhDo
            INNER JOIN ChuyenMon CM ON CV.ChuyenMon_CongViec = CM.Id_ChuyenMon
            INNER JOIN NgoaiNgu NN ON CV.NgoaiNgu_CongViec = NN.Id_NgoaiNgu
            LEFT JOIN KyNang_CTE KNCTE ON CV.Id_CongViec = KNCTE.Id_CongViec
            LEFT JOIN KyNangMem_CTE KNMCTE ON CV.Id_CongViec = KNMCTE.Id_CongViec


SELECT *
FROM CongViec

DELETE LichSu
WHERE id='UV01'

SELECT * FROM FilterUV

SELECT * FROM UngVien WHERE Id_UngVien = 'UV01'

SELECT * FROM TaiKhoan

INSERT INTO TaiKhoan VALUES (N'aaaaaaaaa',N'UV01',N'123',N'user',N'UV01'),
							(N'aaaaaaaab',N'UV02',N'123',N'user',N'UV02'),
							(N'aaaaaaaac',N'UV03',N'123',N'user',N'UV03'),
							(N'aaaaaaaad',N'admin',N'123',N'admin',N'UV05')

SELECT * FROM UngVien

SELECT uv.Id_UngVien, Ten_UngVien, GioiTinh_UngVien, SDT_UngVien, Email_UngVien, DiaChi_UngVien
            FROM UngVien uv

			SELECT Id_NganhNghe, Ten_NganhNghe FROM NganhNghe






UPDATE CongViec
SET CapBac_CongViec = 'CaB05'
WHERE ChuyenMon_CongViec IN (
    SELECT Id_ChuyenMon
    FROM ChuyenMon
    WHERE Ten_ChuyenMon != N'Công nghệ Thông tin'
)

DELETE FROM CongViec
WHERE Id_CongViec BETWEEN 'CV41' AND 'CV90'

DELETE FROM CongViec
WHERE Id_CongViec IN (
    'CV91','CV92','CV93','CV94','CV95','CV96','CV97','CV98','CV99',
    'CV100','CV101','CV102','CV103','CV104','CV105','CV106','CV107','CV108','CV109',
    'CV110','CV111','CV112','CV113','CV114','CV115','CV116','CV117','CV118','CV119',
    'CV120','CV121','CV122','CV123','CV124','CV125','CV126','CV127','CV128','CV129',
    'CV130','CV131','CV132','CV133','CV134','CV135','CV136','CV137','CV138','CV139',
    'CV140'
);


SELECT CV.Id_CongViec, CV.Ten_CongViec,
       CV.MucLuong_CongViec, CB.Ten_CapBac,
       VT.Ten_ViTri, TP.Ten_TinhTP,
       ISNULL(KN.DanhSachKyNang, '') AS KyNang
FROM   CongViec CV
       JOIN ViTriChuyenMon VT ON CV.ViTri_CongViec = VT.Id_ViTri
       JOIN PhuongXa PX        ON CV.KhuVuc_CongViec = PX.Id_PhuongXa
       JOIN QuanHuyen QH       ON PX.Id_QuanHuyen    = QH.Id_QuanHuyen
       JOIN TinhTP    TP       ON QH.Id_TinhTP       = TP.Id_TinhTP
       JOIN CapBac    CB       ON CV.CapBac_CongViec = CB.Id_CapBac
       LEFT JOIN (
         SELECT Id_CongViec, STRING_AGG(KN.Ten_KyNang, ', ') AS DanhSachKyNang
         FROM   ChiTietKyNang CTK JOIN KyNang KN ON CTK.Id_KyNang = KN.Id_KyNang
         GROUP BY Id_CongViec
       ) KN ON CV.Id_CongViec = KN.Id_CongViec

SELECT *
FROM 