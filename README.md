# Over Powered Mod (엽기얼럿 제로)

* This mod is currently for OpenRA release-20161019 (latest stable as of 2017-01-19)
* See wiki for changes in units :)
* You can report bugs at the issues menu.

The following are for modders.

# 모딩 환경 갖추는 법

어렵다...
우선은 OpenRA를 git 으로 받아야 한다.

현재는 release-20161019 tag 를 기준으로 한다:

$ git clone https://github.com/OpenRA/OpenRA.git
$ git checkout release-20161019

게임 본판 엔진과 모드의 버전이 맞지 않으면 고통스러우니까 ㅋ
대부분 rules 수정으로만 했지만 일부 기능의 경우 엔진의 기능이 못 받쳐줘서 직접
코딩을 해서 넣은 부분이 있다 (!)
그래서 이런 고통스런 과정을 거쳐야 하는 것이다.

사실은 직접 하지 않고 다른 모드에서 가져옴.
https://github.com/GraionDilach/OpenRA.Mods.AS
여기 이 모드에 내가 원하는 기능이 꽤 많이 구현이 되어 있다.

각설.

엔진을 다운받았으면 우리 모드도 받아야지.
안에 모드들이 있는 데로 들어간다.
$ cd OpenRA\mods
$ git clone https://github.com/forcecore/yupgi_alert0.git

이제 컴파일 해야 하는 부분을 길들여야 하는데...

# Dependency 설치

게임 엔진의 make.cmd 를 실행한다.
그러면 컴파일 할까? 라고 물어보는데
게임 엔진 본판을 컴파일 하기 전에, dependency부터 설치해야 한다.
다행히 자동으로 됨 ㅋ

make.cmd 실행하고 dependencies 실행.
그럼 설치된다.

그리고 게임 엔진을 컴파일 한다.
역시 make.cmd 실행하고 all 선택. 끝.

# 우리 게임의 확장 DLL 컴파일

이게 하이라이트.
디펜던시 설치가 완료되면
OpenRA.sln
이 비주얼 스튜디오 community edition 에서 열리고,
이전까진 안 되던 컴파일도 정상적으로 잘 될 것이다.
그리고 우리의 프로젝트도 슬쩍 끼워넣자.

눈썰미가 좋은 사람은 알아챘겠지만
OpenRA.Mods.{D2k,RA,RA2,TS} 등이 게임 엔진 폴더에 있을 법한 것이
우리의 모드 폴더에 들어있다는 것이다.
그러면 조금 곤란함. 소프트링크로 해결을 보자.
윈도우니까.
Link Shell Extension 을 설치하라.
http://schinagl.priv.at/nt/hardlinkshellext/linkshellextension.html

mods/yupgi_alert/OpenRA.Mods.yupgi_alert 폴더를 우클릭해서 링크 소스 선택해주자.
그리고 엔진 폴더에 soft link로 만들기를 해주자.
그러면 윈도우는 마치
OpenRA.Mods.{D2k,RA,RA2,TS} 등과 함께 OpenRA.Mods.yupgi_alert 이 있는 것으로 인식할 것이다.

Solution Explorer에서 솔루션에 우클릭 --> add --> existing project 로
소프트링크 안의 프로젝트를 선택해준다.

이제 해당 프로젝트를 컴파일 할 수 있을 것이다.
