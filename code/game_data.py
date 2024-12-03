#고도형 파트 스토리 진행
PLAYER_DATA={
    'Warden' : {1:['구덩이를 파며 자신을 성찰해라','하루에 하나씩','규격은 삽 1개 길이다'],
                2:['오늘도 구멍을 파라'],
                3:['금속 조각을 찾으면 보고하도록'],
                4:['... 돌아가서 구멍을 다시 파라'],
                5:['도마뱀이 나타났다'],
                6:['저희가 숨겨놓은 문서를','수정할 때가 되었습니다'],
                7:['꺼내'],
                8:['총을 훔쳐갔군','어서 가져오지 않으면','선전포고의 의미로','받아들이겠다'],
                9:['내가 패배했다']},
    'zero' : {1:['너의 동료가 되어 줄게','앞으로 잘 지내자','오늘부터 구멍을 파도록 해'],
              2:['오늘도 구멍을 파야 해'],
              3:['캠프 중심으로 가'],
              4:['보물상자를 워든에게 보고해'],
              5:['Mr.sir의 집으로 가서','문서를 훔쳐']},
    'Default':{1:['스탠리는 누명을 써서','이곳에 왔다.','이곳은 뭐하는 곳일까?'],
               2:['여긴 네가 새로운 사람이','될 수 있는 곳이다.','규칙만 잘 따라라'],
               3:['O 버튼을 꾹 누르면','구덩이 파기가 완료됩니다.'],
               4:['1토큰을 획득하였습니다'],
               5:['상점 오픈'],
               6:['어','작은 보물상자를 발견했다.','인벤토리에 넣었다.'],
               7:['문서는 없었다.','대신 총을 챙기자'],
               8:['인벤토리에 열쇠와 문서가 들어왔다.'],
               9:['이 캠프는 특정 보물을 찾기 위해 운영되었으며','무고한 학생들은 법원의 비리로','캠프에 이송되었다.','이 문서를 변호사에게 보내고 나니','다음날 자유가 되었고 워든과 Mr.sir는','높은 형량을 받게 되었다.'],
               10:['엄청난 양의 보물이다!']},
    'Boss':{1:['왕도마뱀이 나타났다'],
            2:['도마뱀 20마리를 죽이자'],
            3:['왕도마뱀을 죽였다','100토큰을 획득하였다.']}
}




#삽이 특정 레벨에 달성하면 점멸 사용가능
TOOL_DATA={
    'Shovel':{
        'level':{
            1:{'plusdamage':1, 'digspeed':1, 'skill':False, 'need_coin':10 },
            2:{'plusdamage':2, 'digspeed':2, 'skill':False,'need_coin':20},
            3:{'plusdamage':3, 'digspeed':3, 'skill':False,'need_coin':30},
            4:{'plusdamage':4, 'digspeed':4, 'skill':False,'need_coin':40},
            5:{'plusdamage':5, 'digspeed':5, 'skill':True,'need_coin':50},
            6:{'plusdamage':6, 'digspeed':6, 'skill':True,'need_coin':60},
            7:{'plusdamage':7, 'digspeed':7, 'skill':True,'need_coin':70},
            8:{'plusdamage':8, 'digspeed':8, 'skill':True,'need_coin':80},
            9:{'plusdamage':9, 'digspeed':9, 'skill':True,'need_coin':90},
            10:{'plusdamage':10, 'digspeed':10, 'skill':True,'need_coin':100}

        },
        'guide':{
            1: 'Camp Green Lake에서 기본으로 제공하는 삽\n땅을 팔 수 있도록 해주는 도구이다\n아직은 약해 보인다',
            2: 'Camp Green Lake에서 기본으로 제공하는 삽\n땅을 팔 수 있도록 해주는 도구이다\n아직은 약해 보인다',
            3: 'Camp Green Lake에서 기본으로 제공하는 삽\n땅을 팔 수 있도록 해주는 도구이다\n어느 정도 쓸만해 보인다',
            4: 'Camp Green Lake에서 기본으로 제공하는 삽\n땅을 팔 수 있도록 해주는 도구이다\n어느 정도 쓸만해 보인다',
            5: 'Camp Green Lake에서 기본으로 제공하는 삽\n땅을 팔 수 있도록 해주는 도구이다\nshift를 눌러보자 꽤 쓸만하다',
            6: 'Camp Green Lake에서 기본으로 제공하는 삽\n땅을 팔 수 있도록 해주는 도구이다\nshift를 눌러보자 꽤 쓸만하다',
            7: 'Camp Green Lake에서 기본으로 제공하는 삽\n땅을 팔 수 있도록 해주는 도구이다\n강해 보인다',
            8: 'Camp Green Lake에서 기본으로 제공하는 삽\n땅을 팔 수 있도록 해주는 도구이다\n강해 보인다',
            9: 'Camp Green Lake에서 기본으로 제공하는 삽\n땅을 팔 수 있도록 해주는 도구이다\n아주 강해 보인다',
            10:'Camp Green Lake에서 기본으로 제공하는 삽\n땅을 팔 수 있도록 해주는 도구이다\n엄청나게 강해 보인다 '

        }
    },
    'Gun':{
        'level':{
            0:{'plusdamage':0, 'digspeed':0, 'skill':False , 'need_coin':10},
            1:{'plusdamage':5, 'digspeed':0, 'skill':False , 'need_coin':20},
            2:{'plusdamage':10, 'digspeed':0, 'skill':False , 'need_coin':40},
            3:{'plusdamage':15, 'digspeed':0, 'skill':False , 'need_coin':80},
            4:{'plusdamage':20, 'digspeed':0, 'skill':False, 'need_coin':160},
            5:{'plusdamage':25, 'digspeed':0, 'skill':True , 'need_coin':320},
            6:{'plusdamage':30, 'digspeed':0, 'skill':True , 'need_coin':640},
            7:{'plusdamage':35, 'digspeed':0, 'skill':True , 'need_coin':1280},
            8:{'plusdamage':40, 'digspeed':0, 'skill':True , 'need_coin':2560},
            9:{'plusdamage':45, 'digspeed':0, 'skill':True , 'need_coin':5120},
            10:{'plusdamage':50, 'digspeed':0, 'skill':True, 'need_coin':10240}

        },
        'guide':{
            0: '아직 쓸 수 없는 아이템,\nMr.Sir을 만나면 얻을 수 있을 것 같다',
            1: 'Mr.Sir에게서 훔친 총,\nYellow-spotted lizard를 잡을 때 사용한다\n아직은 기본적인 공격만 할 수 있다',
            2: 'Mr.Sir에게서 훔친 총,\nYellow-spotted lizard를 잡을 때 사용한다\ 아직은 기본적인 공격만 할 수 있다',
            3: 'Mr.Sir에게서 훔친 총,\nYellow-spotted lizard를 잡을 때 사용한다\ 어느정도 강한 공격을 할 수 있다',
            4: 'Mr.Sir에게서 훔친 총,\nYellow-spotted lizard를 잡을 때 사용한다\ 어느정도 강한 공격을 할 수 있다',
            5: 'Mr.Sir에게서 훔친 총,\nYellow-spotted lizard를 잡을 때 사용한다\ 어느정도 강한 공격을 할 수 있다',
            6: 'Mr.Sir에게서 훔친 총,\nYellow-spotted lizard를 잡을 때 사용한다\ 어느정도 강한 공격을 할 수 있다',
            7: 'Mr.Sir에게서 훔친 총,\nYellow-spotted lizard를 잡을 때 사용한다\ 어느정도 강한 공격을 할 수 있다',
            8: 'Mr.Sir에게서 훔친 총,\nYellow-spotted lizard를 잡을 때 사용한다\ 어느정도 강한 공격을 할 수 있다',
            9: 'Mr.Sir에게서 훔친 총,\nYellow-spotted lizard를 잡을 때 사용한다\ 어느정도 강한 공격을 할 수 있다',
            10: 'Mr.Sir에게서 훔친 총,\Yellow-spotted lizard를 잡을 때 사용한다\ 어느정도 강한 공격을 할 수 있다'
        }
    }
}

ITEM_DATA={
    'HP_potion':{
        'cost':20,'guide':'HP를 50만큼 회복시켜주는 포션'
    },
    'XP_potion':{
        'cost':40,'guide':'XP를 200 얻을 수 있는 포션'
    },
    'THIRST_potion':{
        'cost':20,'guide':'갈증을 20 해소해준다'
    }
}



STAT_DATA={
            0:{'max_hp':100, 'need_xp':100, 'max_thirst':10, 'damage':1, 'digspeed':10},
            1:{'max_hp':120, 'need_xp':0, 'max_thirst':20, 'damage':2,'digspeed':20},
            2:{'max_hp':140, 'need_xp':0, 'max_thirst':30,'damage':3,'digspeed':30},
            3:{'max_hp':160, 'need_xp':0, 'max_thirst':40,'damage':4,'digspeed':40},
            4:{'max_hp':180, 'need_xp':0, 'max_thirst':50,'damage':5,'digspeed':50},
            5:{'max_hp':200, 'need_xp':0, 'max_thirst':60,'damage':6,'digspeed':60},
            6:{'max_hp':220, 'need_xp':0, 'max_thirst':70,'damage':7,'digspeed':70},
            7:{'max_hp':240, 'need_xp':0, 'max_thirst':80,'damage':8,'digspeed':80},
            8:{'max_hp':260, 'need_xp':0, 'max_thirst':90,'damage':9,'digspeed':90},
            9:{'max_hp':280, 'need_xp':0, 'max_thirst':100,'damage':10,'digspeed':100},
            10:{'max_hp':300, 'need_xp':0, 'max_thirst':200,'damage':20,'digspeed':200}
}


