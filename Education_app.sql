-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 10.10.21.103    Database: education_app
-- ------------------------------------------------------
-- Server version	8.0.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `member_test`
--

DROP TABLE IF EXISTS `member_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_test` (
  `ID_Num` int DEFAULT NULL,
  `Test_num` int DEFAULT NULL,
  `Test_result` varchar(45) DEFAULT NULL,
  `Consume_time` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_test`
--

LOCK TABLES `member_test` WRITE;
/*!40000 ALTER TABLE `member_test` DISABLE KEYS */;
INSERT INTO `member_test` VALUES (1,1,'correct',NULL),(1,2,'wrong',NULL),(1,3,'wrong',NULL),(1,4,'correct',NULL),(1,5,'correct',NULL);
/*!40000 ALTER TABLE `member_test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_test_result`
--

DROP TABLE IF EXISTS `member_test_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_test_result` (
  `Num` int NOT NULL,
  `ID_Num` int DEFAULT NULL,
  `Test_result` int DEFAULT NULL,
  `Test_num1` int DEFAULT NULL,
  `num1_result` varchar(45) DEFAULT NULL,
  `Test_num2` int DEFAULT NULL,
  `num2_result` varchar(45) DEFAULT NULL,
  `Test_num3` int DEFAULT NULL,
  `num3_result` varchar(45) DEFAULT NULL,
  `Test_num4` int DEFAULT NULL,
  `num4_result` varchar(45) DEFAULT NULL,
  `Test_num5` int DEFAULT NULL,
  `num5_result` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_test_result`
--

LOCK TABLES `member_test_result` WRITE;
/*!40000 ALTER TABLE `member_test_result` DISABLE KEYS */;
/*!40000 ALTER TABLE `member_test_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `memberinfo`
--

DROP TABLE IF EXISTS `memberinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `memberinfo` (
  `IDnum` int NOT NULL AUTO_INCREMENT,
  `ID` varchar(45) DEFAULT NULL,
  `Password` varchar(45) DEFAULT NULL,
  `User_Name` varchar(45) DEFAULT NULL,
  `Point` int DEFAULT '0',
  `Rank` varchar(45) DEFAULT '4',
  `Division` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`IDnum`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `memberinfo`
--

LOCK TABLES `memberinfo` WRITE;
/*!40000 ALTER TABLE `memberinfo` DISABLE KEYS */;
INSERT INTO `memberinfo` VALUES (1,'ksi','1234','김성일',0,'4','학생'),(2,'kkt','1234','김기태',0,'4','학생'),(3,'lsb','1234','이상복',0,'0','선생'),(5,'jdh','1234','조동현',0,'4','선생');
/*!40000 ALTER TABLE `memberinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `q&a`
--

DROP TABLE IF EXISTS `q&a`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `q&a` (
  `Num` int NOT NULL AUTO_INCREMENT,
  `User_Name` varchar(45) DEFAULT NULL,
  `Date` varchar(45) DEFAULT NULL,
  `Question` varchar(300) DEFAULT NULL,
  `Question_contents` varchar(300) DEFAULT NULL,
  `Answer` varchar(300) DEFAULT NULL,
  `Answer_user` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Num`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `q&a`
--

LOCK TABLES `q&a` WRITE;
/*!40000 ALTER TABLE `q&a` DISABLE KEYS */;
INSERT INTO `q&a` VALUES (1,'김성일','2023-02-07','어려워여','넘나 어려워여','악깡버하라고','이상복'),(2,'김성일','2023-02-08','교수님','진도가 너무 빨라용\n넘 하기시룸','포기하지마시고 따라오세요 ','이상복'),(3,'김성일','2023-02-08','교수님 하기시룸','너무 하기시룸 놀고싶음','응애','이상복'),(4,'김성일','2023-02-08','ㄴㅁㅇㄴㅁㅇ','ㅁㄴㅇㅁㄴㅇㅁㄴㅇ','열심히 하세요','이상복');
/*!40000 ALTER TABLE `q&a` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test` (
  `Test_num` int NOT NULL AUTO_INCREMENT,
  `Test_contents` varchar(1000) DEFAULT NULL,
  `Test_img_URL` varchar(1000) DEFAULT NULL,
  `Test_correct_answer` varchar(45) DEFAULT NULL,
  `Test_subject` varchar(45) DEFAULT NULL,
  `Test_contents_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Test_num`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES `test` WRITE;
/*!40000 ALTER TABLE `test` DISABLE KEYS */;
INSERT INTO `test` VALUES (2,'천연기념물 제 218호인 이 곤충은 무엇인가요? ','http://www.nature.go.kr/fileUpload/photo/O1/ZOBL0003_1.jpg','장수하늘소','곤충','장수하늘소'),(3,'남한에서 제주도에만 분포하고있는 이 나비의 이름은 무엇입니까?','http://www.nature.go.kr/fileUpload/photo/R1/ZREP0016_1.jpg','산굴뚝나비','곤충','산굴뚝나비'),(4,'검정풍뎅이과 중 가장 대형이며 1950년대까지만 해도 서울에서 많이 볼 수 있었던 이 곤충은 무엇인가?','http://www.nature.go.kr/fileUpload/photo/O1/ZOEJ0031_1.jpg','수염풍뎅이','곤충','수염풍뎅이'),(5,'우리나라에 살고 있는 잠자리중 가장 작은 잠자리인 이 곤충은 무엇인가?','http://www.nature.go.kr/fileUpload/photo/D1/ZDAP0008_1.jpg','꼬마잠자리','곤충','꼬마잠자리'),(6,'유충일때 땅 속에 수직굴을 파고 속에 있다가 지나가는 곤충을 잡아먹는 이 곤충은 무엇인가?','http://www.nature.go.kr/fileUpload/photo/O1/ZOBU0004_1.jpg','닻무늬길앞잡이','곤충','닻무늬길앞잡이'),(7,'이 곤충은 무엇인가?','http://www.nature.go.kr/fileUpload/photo/D1/ZDAP0001_1.jpg','대모잠자리','곤충','대모잠자리'),(8,'몸은 황갈색 또는 연한 갈색이며, 앞가슴등판 가운데의 가는 세로 줄과 양 옆의 뒤쪽에 있는 둥근 무늬, 딱지날개의 가운데와 가장자리의 가는 줄 등은 흑색인 이 곤충은?','http://www.nature.go.kr/fileUpload/photo/O1/ZOEC0011_1.jpg','두점박이사슴벌레','곤충','두점박이사슴벌레'),(9,'노란산 잠자리의 몸 색상과 무늬는 암수가 약간 다른데 성숙한 암컷의 날개에는 이 색의 무늬가 더 넓게 퍼져 있다. 이 색은 ? ','http://www.nature.go.kr/fileUpload/photo/D1/ZDAG0009_1.jpg','등황색','곤충','노란산잠자리'),(10,'상제나비는 앞뒤 날개 모두 이 색을 띈다 이 색은 ? ','http://www.nature.go.kr/fileUpload/photo/R1/ZRED0002_1.jpg','흰색','곤충','상제나비'),(11,'고속도로에서 출몰하는 이 동물은 ? ','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000115_001.jpg','고라니','포유류','고라니(골격)'),(12,'고슴도치는 잡식성 동물이다 (O,X로 답해주세요)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000010_001.jpg','O','포유류','고슴도치'),(13,'이 동물의 이름은?','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000105_001.jpg','너구리','포유류','너구리'),(14,'노루는 평야 지대에 서식한다 (O,X로 답해주세요)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000093_001.jpg','X','포유류','노루'),(15,'다람쥐는 야행성이다 (O,X로 답해주세요)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000028_001.jpg','X','포유류','다람쥐'),(16,'담비는 활엽수림에서 서식한다 (O,X로 답해주세요)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000118_001.jpg','X','포유류','담비'),(17,'대륙사슴은 계절에 따라 서식장소가 다릅니다. 봄과 가을에는 초원과 산중 어디에 살까요?','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000116_001.jpg','초원','포유류','대륙사슴'),(18,'이 동물은 무엇인가요 ? ','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000018_001.jpg','두더지','포유류','두더지'),(19,'멧돼지는 무리를 지어 생활한다 (O,X)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000117_001.jpg','O','포유류','멧돼지'),(20,'멧토끼는 1년에 5~6회 이상 번식하며 , 1회에 1~4마리의 새끼를 낳는다 (O,X)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000097_001.jpg','X','포유류','멧토끼'),(21,'이 동물의 이름은?','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000112_001.jpg','물개','포유류','물개'),(22,'사향노루는 매우 긴 꼬리를 가지고 있다 (O,X)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000110_001.jpg','X','포유류','사향노루'),(23,'산양은 귀소성이 없어서 온 산을 돌아다닌다 (O,X)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000119_001.jpg','X','포유류','산양'),(24,'이 동물의 이름은 칡이다 (O,X)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000092_001.jpg','X','포유류','삵'),(25,'수달의 몸은 가늘고 꼬리가 매우 길어 꼬리가 몸통길이의 1.5배이다 (O,X)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000065_001.jpg','X','포유류','수달'),(26,'사진과 같이 호랑이와 같은 줄무늬를 띄고있는 이 동물의 이름은?','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000109_001.jpg','스라소니','포유류','스라소니'),(27,'여우는 굴파기를 좋아해서 여러곳에 굴을 파고 사용한다.(O,X)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000108_001.jpg','X','포유류','여우'),(28,'항문 위에 냄새를 분비하는 기관이 있어 황색의 악취가 나는 액체를 분비하는 이 동물은?','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000089_001.jpg','오소리','포유류','오소리'),(29,'족제비는 암컷이 수컷보다 크다 (O,X)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000043_001.jpg','X','포유류','족제비'),(30,'집쥐의 수명은 야외에서는 1~2년 사육상태에서는 3년이다. (O,X)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000013_001.jpg','O','포유류','집쥐'),(31,'청솔모의 가슴, 배 부위의 털은 일년 내내 검은색이다.(O,X)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000039_001.jpg','X','포유류','청설모'),(32,'한국에서 거의 멸종된 상태인 이 동물은 야행성 동물이다(O,X)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000125_001.jpg','O','포유류','표범'),(33,'하늘다람쥐는 한번의 활공으로 100 m 이상 이동할수 있다.(O,X)','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000023_001.jpg','O','포유류','하늘다람쥐'),(34,'꼬리는 연한 황갈색을 띠면서 여덟 줄의 검은 고리 모양의 가로무늬가 있는 우리나라에서 가장 큰 맹수인 이 동물은?','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000120_001.jpg','호랑이','포유류','호랑이'),(35,'가마우지','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0000896_001.jpg','가마우지','조류','가마우지'),(36,'가창오리','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0000881_001.jpg','가창오리','조류','가창오리'),(37,'이 새는 무엇인가요?','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0000968_001.jpg','갈매기','조류','갈매기'),(38,'개구리매','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0001123_001.jpg','개구리매','조류','개구리매');
/*!40000 ALTER TABLE `test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `학습자료`
--

DROP TABLE IF EXISTS `학습자료`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `학습자료` (
  `분류` varchar(45) DEFAULT NULL,
  `이름` varchar(45) DEFAULT NULL,
  `생태특징` varchar(3000) DEFAULT NULL,
  `일반특징` varchar(3000) DEFAULT NULL,
  `이미지` varchar(3000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `학습자료`
--

LOCK TABLES `학습자료` WRITE;
/*!40000 ALTER TABLE `학습자료` DISABLE KEYS */;
INSERT INTO `학습자료` VALUES ('포유류','고라니(골격)','고라니는 야산(들 근처에 있는 나지막한 산)의 중턱 아래 산기슭이나 강기슭, 억새가 무성한 풀숲 등지에서 살며 계절에 따라 사는 장소를 옮긴다. 봄에는 경작지와 가까운 풀숲, 여름에는 버드나무숲이나 그늘진 냇가, 가을에는 풀숲, 버드나무숲, 곡식 낟가리(낟알이 붙은 볏단이나 보릿단 따위를 쌓아 올린 더미) 속에서 발견되며, 겨울에는 햇볕이 잘 드는 논둑 위에 누워 있는 것을 볼 수 있다. 먹이는 초식성으로 나뭇잎과 연한 풀을 주로 먹으며, 겨울에는 나뭇가지 끝이나 침엽수의 잎, 풀뿌리, 나무뿌리, 보리의 연한 끝을 잘라 먹는다. 물을 매우 좋아하는 습성이 있다.','사슴과 중에 몸이 제일 작다. 위턱에 송곳니가 길게 자라 끝이 구부러져 있으며 입 밖으로 나와 있는 것이 특징이다. 송곳니는 적과 대항할 때 사용하기도 하지만, 나무뿌리를 캐는 도구로써 이용된다. 고라니는 암수 모두 뿔이 없고, 등은 아치형으로 약간 굽어 있다. 머리는 작고 앞이마가 약간 부풀어 있으며, 목은 짧고 엉덩이는 높다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000115_001.jpg'),('포유류','고슴도치','고슴도치는 는 다양한 환경에서 서식한다. 지렁이와 절지동물부터 새의 알과 뱀까지 다양한 동물을 주식으로 먹으며 수박, 오이, 참외 등 과실도 즐겨 먹는 잡식성 동물이다.','한반도산 식충류 중 가장 몸집이 크다. 네 다리는 짧고 몸통은 통통하다. 등과 옆구리 털이 가시와 같은 조직 형태로 변화한 몸 구조를 지닌다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000010_001.jpg'),('포유류','너구리','너구리는 관목(비교적 키가 작은 나무)이 우거지고 습기가 많은 저지대에 서식하며, 산 정상 부근과 산지의 산림에서는 거의 서식하지 않는다. 주로 하천이나 호수 주변의 갈대나 띠(볏과의 다년초)가 떼 지어 나 있는 곳을 선호하며 관목림이나 작은 나무가 흩어져 있는 초지 주변의 농경지 부근, 산지, 산림, 산장 등의 인가 근처에도 자주 나타난다. 들쥐, 개구리, 뱀, 게, 지렁이류, 곤충, 열매, 고구마 등을 먹는다.','우수리너구리와 유사하지만, 털 색깔이 좀 더 거무스레하다. 몸의 털 색깔은 황색이며 얼굴, 목, 가슴과 네 다리는 흑갈색이다. 등 면의 중앙부와 어깨는 끝이 검은 털이 많고, 눈 밑에 흑갈색의 큰 반점이 있다. 몸집이 크고 꼬리는 굵고 짧으며 귀는 둥그렇게 작다. 다리는 매우 짧다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000105_001.jpg'),('포유류','노루','노루는 높은 산 또는 언덕의 산림지대에 서식하며 다른 동물과 달리 겨울철에도 음지에서 서식하는 특징이 있다. 새벽에 주로 활동하며 부드럽고 수분이 많은 풀, 나무의 줄기나 잎(송악, 시로미, 보춘화, 산철쭉, 눈향나무 등)을 즐겨 먹으며 천남성이나 고사리류는 싫어한다.','뿔은 3개의 가지로 나뉘며 돌기는 매우 짧고 가지도 짧다. 귀는 크고, 안하선(눈 밑에 분비작용을 하는 기관)이 없으며, 위턱에 송곳니가 보통 없다. 여름털(온대, 한대에 사는 포유류의 여름에 나는 털)은 황적갈색, 겨울털(온대, 한대에 사는 포유류의 겨울에 나는 털)은 회갈색을 띠며 겨울철에는 엉덩이에 흰 반점이 뚜렷하다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000093_001.jpg'),('포유류','다람쥐','다람쥐는 해안에서 고지대에 이르는 초원, 교목림, 관목림 등 다양한 환경에서 서식한다. 산림지역의 키 큰 나무가 밀집한 곳보다 노출된 환경에서 개체수가 많다. 낮에 활동하는 주행성으로 나무나 풀의 씨, 꽃, 곤충류, 달팽이와 같은 육상조개류 등을 먹는다. 나무 구멍도 이용하지만 동면과 번식은 땅속에 파 놓은 굴에서 한다.','몸집이 작고 네 다리와 귀는 비교적 짧고 꼬리는 편평하다. 볼 안에 큰 볼 주머니가 있어 한 번에 도토리 등의 종자를 열 개 이상 가득 저장하여 운반할 수 있다. 등에는 5개의 검은색 줄무늬가 있고 배면은 희다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000028_001.jpg'),('포유류','담비','담비는 활엽수림에는 서식하지 않고 숲이 울창하여 통과하기 어려운 침엽수림에서만 2-3마리씩 무리 지어 서식한다. 나무를 잘 타고 땅 위를 잘 달리기 때문에 천적을 잘 피하며, 무리 지어 다니면서 자기보다 강한 오소리를 습격하기도 한다. 작은 초식동물이나 설치류, 파충류, 나무열매 등을 먹는다.','담비속에 속하는 동물 중에서 가장 크고, 몸통은 가늘고 길며 꼬리는 몸통 길이의 2/3 정도로 매우 길다. 털의 색깔은 겨울에 황색으로 변하는 것과 황갈색 그대로 있는 것 2가지 형이 있고 몸의 털은 부드럽고 광택이 있다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000118_001.jpg'),('포유류','대륙사슴','일제강점기까지만 해도 대륙사슴은 제주도를 포함한 전국에 분포하였지만, 조선총독부의 해수구제사업으로 멸종되어 자취를 감추었다. 사람의 자취가 드문 산에서 무리 생활을 하며, 울창한 밀림과 바위산에서는 볼 수 없다. 계절에 따라 서식장소가 다른데 겨울에는 눈이 작게 덮인 양지쪽일제강점기까지만 해도 대륙사슴은 제주도를 포함한 전국에 분포하였지만, 조선총독부의 해수구제사업으로 멸종되어 자취를 감추었다. 사람의 자취가 드문 산에서 무리 생활을 하며, 울창한 밀림과 바위산에서는 볼 수 없다. 계절에 따라 서식장소가 다른데 겨울에는 눈이 작게 덮인 양지쪽, 봄과 가을에는 나무가 드문 초원, 여름에는 나무 그늘이 많고 산, 즙액이 풍부한 초원에서 산다. 먹이는 주로 풀, 나뭇잎, 연한 싹, 나무껍질, 도토리, 이끼, 버섯류이다. 새끼는 4~6월에 보통 한 마리, 드물게 두 마리의 새끼를 낳는다.','크기는 노루보다 크며 북한의 백두산사슴보다는 훨씬 작다. 엉덩이의 흰 반점이 백두산사슴과 구별되며, 몸의 반점은 여름보다 겨울에 더 많이 보인다. 여름과 겨울에 몸 색깔의 차이를 보이는데, 여름에는 어두운 회갈색을 보이고, 겨울에는 밝은 갈색을 띤다. 수컷은 암컷보다 1.5배 정도 크다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000116_001.jpg'),('포유류','두더지','한국, 일본, 중국 등지에 분포한다.','몸은 약간 편평한 원통형이며 주둥이는 가늘고 길며, 꼬리는 짧고 통통하다. 털은 촘촘하지 않지만 부드럽고 곧추서 있다, 눈은 퇴화하여 피부 밑에 감쳐져 있고, 귓바퀴가 없다. 팔이라 할 수 있는 앞발은 매우 짧지만, 바닥과 발가락은 크고 튼튼하여 굴을 파는데 유리하다. 몸의 털은 부드럽고 곧추서 있지만, 촘촘하지는 않다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000018_001.jpg'),('포유류','멧돼지','멧돼지는 산림 속에서 서식하며 야행성 활동을 한다. 무리를 지어 생활하며 활엽수가 우거진 곳을 좋아하며 때로는 숲 가장자리의 농경지대로 내려와 농작물 피해를 주는 경우도 빈번하다. 잡식성으로 고사리뿌리, 도토리, 과실을 좋아하고 겨울에는 나무뿌리를 캐어 먹는다. 죽은 동물, 곤충의 번데기, 지렁이도 잘 먹는다. 가을에는 감자, 고구마 등의 농작물을 캐어 먹는 등 적응력이 강하고 행동이 민첩하다.','돼지와 비슷하나 몸이 더 크다. 머리는 긴 원추형이며 뚜렷한 경계 없이 짧고 굵은 목과 붙어 있다. 삼각형인 귓바퀴는 빳빳하게 일어서 있고 눈이 매우 작고 다리는 굵고 짧다. 털은 흑갈색을 띠며 나이가 들수록 희미해진다. 날카로운 송곳니가 있어서 질긴 나무뿌리를 자르거나 싸울 때 사용한다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000117_001.jpg'),('포유류','멧토끼','멧토끼는 전국의 야산(들 근처에 있는 나지막한 산), 평야, 농경지에서 산악 산림지대에 이르는 다양한 환경에서 서식한다. 초식성으로 식물의 종자나 줄기를 즐겨 먹으며, 겨울철 먹이가 부족할 시기에는 어린나무의 껍질을 먹기도 한다. 1년에 2-3회 번식하며, 1회에 1-4마리의 새끼를 낳는다.','토끼류 가운데 중소형에 속하며, 몸의 색은 일반적으로 다갈색이 대부분이다. 여름과 겨울에 털의 색은 변함이 없으나 겨울털은 일반적으로 길고 부드럽고 빽빽하게 나 있으며 여름털은 거칠고 짧다. 나이가 들거나 서식 환경에 따라 약간 변이가 있고, 주로 옅어지는 경향이 있다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000097_001.jpg'),('포유류','물개','물개는 우리나라에서 겨울에 동해를 거쳐 남해 또는 서해 남부에 나타난다. 여름과 가을에 바위 지역의 해변에서 서식하며 대부분 시간을 바다에서 보낸다. 주로 오징어, 청어, 명태, 정어리 등 어류와 갑각류 등을 잡아먹는다.','태어날 때에는 검은색이지만 나이를 먹을수록 등 면은 짙은 갈색 또는 회흑색으로 변한다. 성숙한 수컷에게는 거친 보호 털이 있으며, 목, 가슴, 등이 특히 짙다. 앞다리와 뒷다리 모두 지느러미 모양이며 꼬리는 매우 짧다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000112_001.jpg'),('포유류','사향노루','바위가 많고 1,000m 이상 되는 높은 산의 침엽수림 또는 침엽수나 활엽수가 혼재하는 숲에서 단독이나 작은 집단을 형성하여 생활한다.','고라니와 비슷하며, 수컷은 약 50㎜나 되는 송곳니가 입 밖으로 약간 나와 있다. 매우 짧은 꼬리는 겉에서 잘 보이지 않는다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000110_001.jpg'),('포유류','산양','산양은 접근하기 어려운 바위 등의 험한 산악 산림지대에서 서식한다. 귀소성(동물이 먼 곳에 갔다가도, 살던 집이나 둥지로 돌아오는 성질)이 매우 강하고 한번 정한 서식지에서 오랫동안 서식한다. 일반적으로 단독 생활을 하거나 10마리 이내의 가족 단위로 무리를 지어 바위 사이나 동굴에서 생활하며 주로 새벽과 저녁에 활동한다. 먹이로는 풀, 산열매, 도토리, 바위 이끼, 보리수, 포도, 진달래, 철쭉, 신갈나무, 피나무 등의 잎이며, 겨울철에는 나무껍질, 침엽수의 잎, 지의류, 억새 등을 먹는다.','외국산 산양과 달리 얼굴 선이 없다. 염소와 비슷하지만, 턱에 수염이 없고, 몸통이 두껍다. 암수 모두 뒤쪽으로 굽은 작은 뿔이 있다. 목이 짧고 다리는 굵고 발끝이 뾰족하고 험한 바위에서 서식하기에 적합한 발굽을 가지고 있다. 몸체의 털은 회갈색이지만 일부 털의 끝은 옅은 흑갈색이다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000119_001.jpg'),('포유류','삵','삵은 산림지대의 계곡, 바위굴, 연안, 관목(비교적 키가 작은 나무)으로 덮인 산골짜기 개울가에서 주로 살며, 마을 근처에서 살기도 한다. 단독 또는 한 쌍으로 생활하며, 야행성이지만, 골짜기의 외진 곳에서는 낮에도 먹이를 찾아다닌다. 먹이는 주로 쥐 종류와 작은 동물, 꿩 새끼, 멧토끼, 청설모, 다람쥐, 닭, 오리, 곤충 등을 잡아먹기도 한다.','식육목에 속하며 고양이처럼 생겼으나 고양이보다 몸집이 크고 불분명한 반점이 많다. 입을 크게 벌릴 수 있고 머리는 둥글며, 턱의 근육이 발달하여 먹이나 다른 물건을 물어뜯는 힘이 매우 세다. 꼬리에는 고리모양의 가로띠가 있으며 눈 위 코로부터 이마 양쪽에 흰 무늬가 뚜렷하게 나타난다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000092_001.jpg'),('포유류','수달','수달은 다른 포유동물과 달리 강과 육지를 이용하며 전국 하천, 계곡, 호수, 저수지 일대와 인근 연안의 도서지방에 널리 분포하고 있다. 하천이나 호숫가에 살며 물가에 있는 적이 쳐들어오는 것을 막을 수 있는 구멍 또는 나무뿌리 밑이나 땅에 구멍을 파고 산다. 몸은 수중생활을 하기에 좋도록 적응되어 있다.','몸은 가늘고 꼬리는 매우 길어 몸통길이의 2/3 정도이다. 다리는 짧고 발가락 사이에 물갈퀴가 발달하여 헤엄치기에 편리해져 있다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000065_001.jpg'),('포유류','스라소니','국제적으로 멸종 위기에 처해 있는 동물로 유라시아에 걸쳐 서식하는 종이다. 높은 산의 밀림 속에서 살며 대개 야행성이다. 행동이 민첩하고 활동 범위가 넓으며, 나무에도 잘 오른다. 먹이는 쥐, 멧토끼, 꿩, 어치, 닭, 사슴, 어린 멧돼지, 사향노루 등이며 가축을 습격하기도 한다. 일반적으로 새끼는 2~3마리 정도이나 1~5마리까지도 낳는다. 새끼의 양육은 암컷이 전담하며 수명은 12-15년에 이른다.','고양이나 삵과 비슷하나 꼬리가 뭉툭하며 짧은 것이 특징이다. 크기는 고양이와 표범의 중간 정도이며, 약간 통통하다. 무늬는 호랑이와 같은 줄무늬를 띠고 색깔은 어두운 누른빛 또는 회갈색에 불명확한 갈색 무늬가 있다. 귀는 다른 고양이과 동물에 비해 뾰족하고 끝 부분에 긴 털이 나 있다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000109_001.jpg'),('포유류','여우','여우는 늑대보다 인가 주변에서 자주 관찰되었던 동물이나 절종 위기에 있다. 산림, 초원, 마을 부근 등에 있는 바위틈이나 흙으로 된 굴에서 사는데, 스스로 굴을 파기도 하지만, 굴 파기를 싫어해서 오소리의 굴을 빼앗아 쓴다. 주로 새벽과 저녁에 활동을 많이 하며 야산의 노출된 환경에서 놀기를 좋아한다.','개과의 동물 중 몸통의 길이에 비해 꼬리 길이가 긴 점과 주둥이 부위가 가늘고 예리한 것이 특징이다. 털의 색깔은 개체에 따라 다르나 보통은 몸 윗면이 황색인데, 이마와 등 부분의 털끝이 희므로 희끗희끗하게 보인다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000108_001.jpg'),('포유류','오소리','오소리는 해가 잘 비치는 나무가 드문 산림이나 관목림, 언덕의 계곡 주변에 굴을 파거나 바위굴을 이용해서 생활한다. 강한 발톱을 가진 앞발로 구멍을 파서 생활하는 특징을 가지고 있다. 곤충, 개구리, 뱀, 지렁이, 쥐와 작은 새 등 동물성인 것뿐 아니라, 식물의 뿌리, 열매와 버섯 등도 먹는 잡식성이다.','몸은 크고 비대하며 얼굴은 원통형이고 주둥이는 뭉툭하다. 털은 거칠고 끝이 가늘며 뾰족하다. 털색은 회색 또는 갈색인데 배면은 암갈색이고 얼굴에는 뚜렷한 검은색과 흰색의 띠가 있다. 콧등은 길며 먹이를 찾는 데 사용하고, 발에는 큰 발톱이 있어 땅굴 파기에 알맞다. 항문 위에 냄새를 분비하는 기관이 있어 황색의 악취가 나는 액체를 분비한다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000089_001.jpg'),('포유류','족제비','족제비는 전국 어디에서나 흔히 볼 수 있는 작은 동물이며, 산림지대의 바위와 돌이 많은 계곡에서 주로 생활한다. 겨울에는 인가 근처의 창고에서 살며 죽은 나무 와 나무뿌리 밑, 돌담 사이 구멍에 보금자리를 만든다. 먹이는 서식환경에 따라 다르나 여름철에는 곤충류, 갑각류, 어류, 파충류, 조류, 포유류 등이며 나무 열매도 먹는다.','다리는 짧고 몸은 길다. 수컷이 암컷보다 크며, 겨울털은 길고 몸 윗면, 사지, 꼬리는 황색을 띠며 이마는 거무스레한 갈색, 뺨과 몸 아랫면은 짙은 황토색을 띤다. 발가락 사이에는 물갈퀴가 있으며 항문의 양쪽에는 악취를 내는 기관이 있다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000043_001.jpg'),('포유류','집쥐','잡식성으로 주로 야간에 활동하지만, 어두운 곳에서는 주간에도 활동한다. 수명은 야외에서는 1-2년이고, 사육 상태에서는 3년이다.','등은 갈색 또는 회갈색이며 배면은 회색이다. 꼬리 길이는 머리와 몸길이보다 길지 않고 꼬리의 비율은 68~99%로 100%를 넘지 않는다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000013_001.jpg'),('포유류','청설모','청설모는 저지대 평지 산림에서 아 고산지대 산림에 걸쳐 서식한다. 적어도 일부는 상록침엽수가 있는 산림을 선호한다. 주행성으로 주로 나무 위에서 활동하며, 지상에서 활동하는 시간은 매우 적다. 호두, 잣 등의 종자, 과실, 버섯, 곤충 등을 먹는다. 겨울철 먹이부족을 위해 가을에는 도토리 등의 종자를 땅속에 저장하거나 바위와 나무 틈새에 감추어 두는 습성이 있다.','입 아래와 가슴, 배 부위의 털은 일 년 내내 순백색이다. 여름털(온대, 한대에 사는 포유류의 여름에 나는 털)에 비해 겨울털(온대, 한대에 사는 포유류의 겨울에 나는 털)은 2배 정도 길고 털의 수도 많다. 특히, 겨울에는 귀에 4㎝가량의 길고 총총한 털이 자라나 외형상으로 여름털과 뚜렷한 차이를 나타낸다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000039_001.jpg'),('포유류','표범','한국에서는 거의 멸종된 상태이다. 대개 고산 지대의 산림 속에서 살며, 해가 진 뒤나 새벽에 활동한다. 나무에도 잘 오르고 헤엄도 친다. 노루, 멧돼지 새끼, 멧토끼 등을 주로 포식하며, 먹이가 부족하면 조류나 쥐 종류도 먹는다. 교미 시기는 겨울이나 봄이며, 교미 후 약 100일 뒤에 보통 2마리의 새끼를 낳는다. 수명은 12년 정도이다.','호랑이보다 몸의 크기는 작지만 더 길쭉하고 가늘다. 꼬리는 가늘고 길어서 몸통 길이의 1/2보다 길다. 머리는 크고 둥글며 수염은 짧다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000125_001.jpg'),('포유류','하늘다람쥐','하늘다람쥐는 전국 산악지대의 자연림 또는 일부 20년 이상 된 인공조림지에서 서식한다. 소형이고 야행성 동물로 한 번의 활공(바람을 써서 공중을 미끄러져 나는 일)으로 통상 20-30m, 때로는 100m 이상도 이동할 수 있다. 집은 딱따구리가 파놓은 나무구멍을 수리하거나 인공 새집을 이용한다. 나무껍질, 잎, 눈, 종자, 과실, 버섯 등의 식물성 먹이를 먹는다.','체구보다 눈망울이 크고, 앞과 뒷발 사이에 피북막이 발달한 비막(척추동물에서 볼 수 있는 비행에 사용되는 막)을 지니고 있다. 등은 옅은 회색 계통과 갈색 계통이 있다. 배면은 백색이고 눈 주위는 흑갈색이다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000023_001.jpg'),('포유류','호랑이','한국에서한국에서는 멸종된 것으로 간주하고 있다. 먹이를 찾아서 하루 80-90㎞ 정도를 돌아다닐 정도로 행동 범위가 넓다. 높은 산의 밀림 지대에서만 산다.','우리나라에 서식하고 있는 맹수 가운데에서도 가장 큰 종류이다. 머리가 크고 사지는 강대하며, 꼬리 길이는 몸통 길이의 1/2 정도이다. 귓바퀴는 짧고 둥글다. 몸 윗면은 선명한 황갈색이고 24개의 검은 가로무늬 줄이 있다. 꼬리는 연한 황갈색을 띠며, 여덟 줄의 검은 고리 모양의 가로무늬가 있다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-MM-0000120_001.jpg'),('곤충','산굴뚝나비','7월에서 8월에 걸쳐 연 1회 발생. 1300m 이상에서 정상에 이르는 초지에 서식한다. 수컷은 화산암 위에서 쉬고 있을 때가 많고, 솔체꽃,송이풀,꿀풀 등에서 흡밀할 때도 있다. 바람이 불면 멀리 나나 보통 인기척에 의해 5-6m 날아가는 경우도 있다.','날개 편 길이 47mm 내외. 암컷은 수컷보다 크고 날개색이 다소 옅다. 남한에서는 유일하게 제주도에 분포하는 종으로, 한국,일본,중국,극동 러시아에서 유럽 등지에 분포한다.','http://www.nature.go.kr/fileUpload/photo/R1/ZREP0016_1.jpg'),('곤충','상제나비','일반적으로 나무가 별로 없는 구릉이나 개살구가 야생화된 지역에 서식하는 것으로 알려져 있으나, 최근 거의 채집되지 않고 있는 종이다. 5월중순에서 6월초에 걸쳐 연 1회 발생한다.','앞뒤 날개모두 흰색을 띠는데 전반적으로 발달된 무늬는 없다. 최근 그 개체수가 줄어들고 있는 희귀종이다.','http://www.nature.go.kr/fileUpload/photo/R1/ZRED0002_1.jpg'),('곤충','수염풍뎅이','성충은 늦봄부터 가을까지 볼 수 있으나 주로 6-7월에 많으며, 밤에 불빛을 보고 날아오는 경우가 있다고 알려져 있다. 유충은 당 속에서 소나무류,사시나무류,갈참나무,참나무 등의 뿌리를 갉아 먹는 것으로 보고되어 있다. 주요분포지역은 한국(북한, 중부, 제주도)만주,몽고,일본 등이며, 1950년대까지는 서울에서도 많이 볼 수 있었으나 1970년대 이후에는 거의 관찰되지 않고 있는 종이다.','중국, 일본에 분포하며, 검정풍뎅이과 중 가장 대형이며, 촉각은 10마디인데 수컷의 곤봉부는 7마디로서 매우 길고 굽었으며, 암컷은 5-6마다이며 직선형이다. 전경절 외치는 2-3개이며, 보통 암, 수 모두 안쪽에 가시가 있는 점이 특징이다. 몸은 굵고 긴 타원형으로 서 짙은 적갈색이나 등쪽에는 매우 짧은 회백색 내지 황백색 털이 얼룩무늬처럼 덮여있다. 수컷의 촉각 곤봉부는 앞가슴등판 길이의 약 1.5배이며, 중간이 굽었고, 암컷은 6마디인데 자루의 길이보다 짧다.','http://www.nature.go.kr/fileUpload/photo/O1/ZOEJ0031_1.jpg'),('곤충','장수하늘소','수령이 오래 된 서어나무 노목들이 자생하고 있는 곳에 서식한다. 성충은 6~9월에 나타나며, 수피에 구멍을 뚫고 한 알씩 산란한다. 유충은 목질부를 식해한다. 유충 기간은 불명하나 3~5년인 것으로 추정된다.','구북구 지역에서 가장 큰 하늘소로, 수컷이 암컷에 비해 몸이 크다. 머리와 가슴은 흑색이고 날개는 적갈색이며 배는 황색 잔털로 덮여 있다. 큰턱은 크고 튼튼하게 생겼으며 위로 구부러져 있고 바깥 쪽에 1개의 가지가 있다. 앞가슴등판의 옆가장자리에는 톱니 모양의 돌기가 나 있으며, 등판에는 황갈색의 털뭉치가 있다.\r\n   우리 나라에서는 현재 그 서식지가 극히 국한되어 있으며, 우리 나라에서 서식하는 곤충 중 유일하게 천연기념물 제218호로 지정되어 있다.','http://www.nature.go.kr/fileUpload/photo/O1/ZOBL0003_1.jpg'),('곤충','깊은산부전나비','문헌에 의하면 6월에서 8월에 걸쳐 연 1회 발생하는 것으로 기록되어 있으며, 대개 높은 위치의 참나무 잎 위에서 활동하므로 발견하기가 쉽지 않다. 수컷은 간혹 오전에 낮은 위치의 잎이나 풀 위에서 일광욕을 하며 오후 늦게는 산의 능선에서 높게 날아다니면서 상승기류를 타고 정상까지 날아오르기도 한다. 암컷은 드물게 큰까치수영의 꽃에서 흡밀한다. 주요 분포지역은 한국, 중국 서부, 극동 러시아 등지이며, 남한에서는 충청남도 계룡산, 경상북도 소백산, 강원도의 높은 산지의 잡목림이나 그 주변 계곡에 서식하는 것으로 알려져 있다.','날개편 길이는 35mm 내외이다. 암컷이 수컷보다 크기가 큰 것 외에 무늬에 의한 구별은 어렵다. 배끝을 조사하는 것이 확실하다.','http://www.nature.go.kr/fileUpload/photo/R1/ZRDG0054_1.jpg'),('곤충','꼬마잠자리','문헌 기록에 의하면 6월에서 8월에 걸쳐 발생하는 것으로 알려져 있다. 미성숙 개체는 우화 후 15-20일이 지나면 성숙해진다. 교미 후 암컷은 혼자서 늪지대, 농수로, 휴경 물논을 돌아다니며 산란을 한다고 알려져 있다.','성충의 몸길이는 11-13 mm, 뒷날개 길이는 13-15 mm이다. 우리 나라에 살고 있는 잠자리 중 가장 작기 때문에 꼬마잠자리로 명명되었다. 암수 모두 날개는 투명하고, 각 날개 밑부분의 삼각실 바깥까지는 등적색이다.','http://www.nature.go.kr/fileUpload/photo/D1/ZDAP0008_1.jpg'),('곤충','노란잔산잠자리','일반적인 생태적 특징은 잘 알려지지 않았다.','배길이 55~60mm, 뒷날개길이 45~50mm. 전체적으로 흑색 바탕에 황색 줄무늬가 있는 큰 잠자리임. 성숙한 수컷의 가슴은 금속성이 강한 흑청록색이며 겹눈은 청남색임. 잔산잠자리와 비슷한 생김새이나 배마디의 황색 무늬가 선명하고 교미 부속기의 미모가 더 짧음. 몸 색상과 무늬는 암수가 약간 다르며 성숙한 암컷의 날개에는 등황색 무늬가 넓게 퍼짐.','http://www.nature.go.kr/fileUpload/photo/D1/ZDAG0009_1.jpg'),('곤충','닻무늬길앞잡이','성충은 여름에 바닷가에서 주로 활동하며, 문헌 기록에 의하면 유충은 다른 길앞잡이류처럼 땅 속에 수직굴을 파고 그 속에 있다가 지나가는 곤충을 잡아 먹을 것으로 추정된다고 한다.','기록에 의하변 몸길이는 12-15 mm 가량이며, 등쪽은 구릿빛 갈색 또는 녹색을 띠며, 배쪽은 녹색의 광택이 있다. 딱지날개의 중앙에 있는 한 쌍의 긴 세로 줄 무늬와 바깥쪽 가장자리의 무늬는 황색이다.','http://www.nature.go.kr/fileUpload/photo/O1/ZOBU0004_1.jpg'),('곤충','대모잠자리','일반적인 생태적 특징은 잘 알려지지 않았다.','배길이 27mm, 뒷날개길이 33mm. 머리는 흑색이고 뒷머리, 이마혹, 이마, 이마조각, 윗입술조각, 윗입술, 아랫입술은 황갈색임. 가슴은 황색을 띈 흑갈색인데 흑갈색 털이 밀생함. 가운데가슴과 가슴 옆면은 황갈색이며 민무늬임. 미부 상부기는 갈색이고 9마디와 길이가 같으며 하부기는 황갈색이며 편평하고 위는 예리하고 위로 구부러짐. 날개는 투명하고 현저한 흑갈색 무늬가 날개의 밑, 가운데, 끝에 있음. 날개맥은 흑갈색이고 가두리무늬는 갈색임.','http://www.nature.go.kr/fileUpload/photo/D1/ZDAP0001_1.jpg'),('곤충','두점박이사슴벌레','일반적인 생태적 특징은 잘 알려지지 않았다.','몸은 황갈색 또는 연한 갈색이며, 앞가슴등판 가운데의 가는 세로 줄과 양 옆의 뒤쪽에 있는 둥근 무늬, 딱지날개의 가운데와 가장자리의 가는 줄 등은 흑색이다.','http://www.nature.go.kr/fileUpload/photo/O1/ZOEC0011_1.jpg'),('조류','가마우지','배가 들어오는 곳, 암초가 많은 해안의 절벽에서 생활한다. 둥지는 암초나 바위 절벽의 층을 이룬 오목한 곳에 마른풀이나 해초를 이용하여 만든다. 알을 낳는 시기는 5월 하순~7월이다. 알은 엷은 청색으로 4~5개 낳는다. 어미 새는 입에서 먹이를 토해 새끼에게 준다. 먹이로는 어류를 즐겨 먹는다. 울음소리는 민물가마우지와 비슷하나, 목을 진동시켜 낮은 소리를 낼 때도 있다. 번식기 이외에는 거의 울지 않는다.','암컷과 수컷 모두 몸의 윗면은 검은색이며 등의 양쪽과 어깨는 구릿빛 녹색을 띤다. 허리와 위 꼬리 덮깃은 녹색의 금속광택이 있고, 매년 1월경에는 허리 양쪽에 크고 흰 얼룩무늬가 생긴다. 부리 주위에는 황색의 피부가 드러나 있으며, 드러난 곳 바깥쪽 얼굴과 턱 아래 부위는 흰색 바탕에 검은 녹색의 얼룩무늬가 흩어져 있다. 매년 1월경에는 머리꼭대기, 뒷머리, 목에 흰색의 장식 깃이 여러 개 생긴다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0000896_001.jpg'),('조류','가창오리','늪지대나 초원 등에서 각종 식물의 열매나 작은 곤충 등을 먹으며, 겨울에는 주로 논에 떨어진 벼 이삭이나 기타 식물의 열매나 잎과 줄기 등을 먹는다. 시베리아 평원지대에서 번식하며 주변의 풀잎 등을 이용하여 둥지를 만든다. 우리나라에서는 10월부터 이듬해 3월까지 겨울을 보낸다. 큰 무리를 이루어 행동하며 일몰 직후 밤에 먹이를 먹으려고 전체의 무리가 비상하는 것이 특징이다. 러시아의 시베리아 동부 등에서 번식하고, 한국, 중국, 일본 등지에서 겨울을 난다.','전체적으로 다갈색이며 번식 후 변환 깃은 수컷과 암컷이 비슷하나 암컷은 부리와 양쪽 뺨이 만나는 곳에 흰색의 원형 반점 있다. 겨울 깃털(번식 깃털)은 수컷은 머리꼭대기가 검은색을 띠나 양쪽 뺨에는 노란색과 녹색 그리고 검은색이 발달 또는 태극모양으로 조화를 이루고 있으며 아래 꼬리 덮깃은 검은색을 띤다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0000881_001.jpg'),('조류','갈매기','해안의 풀밭, 작은 섬 등에서 모여서 번식하며 키 작은 나무의 가지, 마른풀, 해초류 등으로 둥지를 만든다. 엷은 황갈색 및 엷은 푸른색에 어두운 적갈색의 무늬가 흩어져 있는 타원형의 알을 2~3개 낳는다. 유라시아 북부, 영국, 아프리카, 캐나다 서부에서 번식하고 우리나라에는 흔한 겨울새이며 동해안, 남해안, 낙동강하구, 한강 등지에서 볼 수 있다.','머리와 몸의 밑면은 백색이다. 등은 청회색이고 부리와 다리는 녹황색이다. 날 때에 날개 끝에 흑색의 반점이 눈에 띈다. 겨울에는 머리에 줄무늬가 약간 있다. 어린 새는 회갈색이며 다리는 검은색이고 꼬리 끝에 검은색의 띠가 있다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0000968_001.jpg'),('조류','개개비','물가의 풀밭이나 갈대밭에 찾아온다. 일정한 자기 영역을 갖지만, 그 범위가 좁다. 풀 사이를 옮겨다니면서 먹이를 찾으며, 땅 위에 내려오는 경우는 드물다. 둥지는 물가 갈대밭의 갈대 줄기 사이에 만든다. 알을 낳는 시기는 5~8월이다. 알은 엷은 청록색 또는 푸른색이 있는 잿빛의 흰 바탕에 갈색 또는 검은 갈색과 엷은 자색의 얼룩점이 있으며, 4~6개 낳는다.','암컷과 수컷모두 몸 윗면이 엷은 황색을 띤 올리브 갈색이지만, 허리와 위꼬리덮깃은 약간 엷은 색이다. 눈썹선은 황색을 띤 흰색으로 가늘고 명확하지 않으며, 귀깃은 등 깃털과 유사한 색이지만 한층 엷은 색이다. 턱밑, 턱 아래 부위, 윗가슴은 황색을 띤 흰색이며, 턱 아래 부위와 가슴에는 올리브색을 띤 잿빛의 세로 얼룩무늬가 있다. 기타 몸 아랫면은 엷은 크림색이 도는 황갈색이다. 봄철에 털갈이하여 여름 깃으로 바뀌지만, 깃털 색은 겨울 깃과 같다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0000028_001.jpg'),('조류','개구리매','평지의 초원, 습지, 갈대밭 등에 서식하며 둥지는 물풀의 줄기와 잎 등을 이용하여 만든다. 엷은 푸른색의 알을 4~5개 낳는다. 유럽 및 러시아의 시베리아 지방, 중국, 한국, 일본 등지에 분포한다. 넓은 농경지나 갈대밭에서 겨울에 종종 관찰된다.','수컷의 깃털 색은 변이가 많다. 암컷은 갈색 바탕에 담갈색이나 흑갈색의 점이 있다. 암컷과 어린 새는 비슷한 색으로 암갈색을 띤다. 그리고 머리꼭대기와 어깨는 담황색이다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0001123_001.jpg'),('조류','개꿩','해안의 간척지, 하구, 삼각주, 해안가의 풀이 우거진 습지 등에 찾아온다. 날아갈 때는 옆으로 길게 또는 V자 모양으로 줄을 짓는다. 번식은 가장 북쪽의 툰드라 지대에서 한다. 둥지는 땅 위에 만들며, 안에 나무의 작은 가지, 잎, 이끼 등을 깐다. 알을 낳는 시기는 6월 하순~7월 상순이다. 알은 올리브 회색에 검은색의 얼룩무늬와 얼룩점이 있으며, 4개 정도 낳아 23~27일 동안 품는다.','여름 깃은 암컷과 수컷 모두 이마가 흰색이며, 머리꼭대기 뒷부분부터 허리까지는 검은색으로 각 깃의 가장자리는 흰색이다. 위꼬리덮깃은 흰색이며, 검은색의 가로띠가 있다. 눈 위에는 흰색의 눈썹 선이 있고, 이것은 목 옆을 지나 턱 아래 부위와 가슴 양쪽에 있는 흰색의 얼룩무늬로 연결된다. 눈앞, 귀 깃, 턱밑, 턱 아래 부위, 가슴, 윗배는 검은색이며, 아랫배는 흰색이다. 부리는 검은색이고, 다리는 시멘트 색을 띤 검은색이다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0000960_001.jpg'),('조류','개똥지빠귀','울창한 삼림에 찾아온다. 둥지는 작은 나무의 가지 위에 마른풀을 이용해서 밥그릇 모양으로 만든다. 알을 낳는 시기는 5~6월 중순이다. 알은 청록색 바탕에 붉은 갈색의 얼룩점이 있으며, 4~5개 낳는다.','수컷의 겨울 깃은 허리를 제외한 기타 몸 윗면이 어두운 갈색과 검은 갈색이다. 머리꼭대기와 뒷목의 각 깃털의 가장자리는 어두운 잿빛 황갈색이다. 등과 어깨의 가장자리는 밤색으로 개체에 따라 모양이 다양하다. 허리는 검은색을 띤 밤색으로 가장자리가 어두운 잿빛 황갈색이다. 넓은 눈썹 선은 크림색이 도는 흰색이다. 턱밑과 턱 아래 부위는 크림색이 도는 흰색으로 어두운 갈색의 얼룩점이 흩어져 있다. 가슴과 옆구리는 다양한 모양의 밤색을 띤 검은색이다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0000833_001.jpg'),('조류','개미잡이','개미잡이는 마을 주변의 나무에서 볼 수 있다. 나무 줄기의 썩은 부분은 부리로 떼어 내고 송곳으로 비비듯이 긴 혀를 빠르게 뻗어 개미를 잡아 먹는다. 둥지는 나무 구멍(수동), 나무 줄기의 벌어진 틈 사이, 딱다구리의 옛 둥지를 이용한다. 6~7월에 6~7개의 흰색의 알을 낳는다. 먹이는 딱정벌레, 벌, 나비 등과 같은 곤충류나 거미류이다.','개미잡이는 참새보다 몸집이 조금 크고 위면은 회갈색, 아랫면은 황갈색 바탕에 검은색의 조밀한 무늬가 있다. 검은색의 눈선과 머리꼭대기에서 등까지 이어진 검은색 세로줄이 뚜렷하다. 딱다구리와 형태와 생태가 다르며, 나무줄기를 오르기는 하지만 보통 산새처럼 나뭇가지에 수평으로 앉는다. 먼 거리에서는 전체가 회갈색으로 보인다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0000414_001.jpg'),('조류','검독수리','높은 산부터 낮은 산에 이르기까지 넓은 범위에서 생활하며, 일년 내내 암수가 함께 지낸다. 먹이를 발견하여 습격할 때는 날개를 반쯤 접고 전속력으로 미끄러지듯이 날아 낚아챈다. 삼킨 먹이 중에서 소화가 되지 않는 것은 작은 공 모양으로 토해낸다. 둥지는 사람이나 다른 동물이 접근할 수 없는 절벽의 오목한 곳에 마른 가지를 쌓아 올려 만들며, 해마다 동일한 것을 보수하여 이용한다. 알을 낳는 시기는 3월 중순-4월 상순이다. 알은 청백색 바탕에 적갈색의 얼룩무늬가 있으며 2개 낳는다.','암컷과 수컷 모두 머리꼭대기, 뒷머리, 목 옆의 깃이 버들잎 모양이며 어두운 갈색으로, 각 깃의 끝은 황갈색이다. 등, 어깨, 허리는 검은 갈색이며, 그 외의 것은 엷은 색이다. 턱밑, 턱 아래 부위, 몸의 아랫면도 검은 갈색이며, 특히 아랫면이 윗면보다 적게 닳기 때문에 더욱 진한 색이다. 갈고리 모양으로 밑으로 굽은 부리는 검은색이며, 뒷부분은 엷은 색을 띤 회색이다. 다리의 깃털은 어두운 갈색이다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0001124_001.jpg'),('조류','검둥오리사촌','번식지에서는 툰드라나 산림지대의 담수 못, 물이 고인 곳, 하천 등에서 서식한다. 겨울을 나는 곳에서는 큰 무리를 지어 바다 위에서 생활한다. 해면 가까이 낮게 수십 마리가 일렬종대로 날아가는 것을 관찰할 수도 있다. 둥지는 풀숲 속 땅 위에 풀잎과 줄기를 이용하여 접시 모양으로 만든다. 알을 낳는 시기는 5월 하순~6월 상순이다. 알은 크림색으로 8~10개 정도 낳아 27~28일 동안 품는다.','수컷의 겨울 깃은 몸 전체가 검은색이다. 암컷은 이마, 머리꼭대기, 뒷머리, 뒷목이 진한 갈색이며, 얼굴, 목 옆은 흰색을 띤 갈색이다. 등, 어깨 깃, 허리, 위 꼬리 덮깃은 어두운 갈색이며, 가슴, 배, 옆구리는 갈색이다. 암수의 부리는 검은색이나 수컷의 윗부리 뒷부분에는 황색의 솟아 나온 부분이 있다. 다리는 어두운 연한 회색을 띤 갈색이다.','http://www.nature.go.kr/fileUpload/animals/basic/KNAM-BI-0000869_001.jpg');
/*!40000 ALTER TABLE `학습자료` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-08 20:53:03
