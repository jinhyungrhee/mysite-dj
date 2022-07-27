from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category, Tag

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        # 작성자(author) 데이터 생성
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')
        # obama만 staff로 설정
        self.user_obama.is_staff = True
        self.user_obama.save()
        # 카테고리 데이터 생성
        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')
        # 테그 데이터 생성
        self.tag_python_kor = Tag.objects.create(name='파이썬 공부', slug='파이썬-공부')
        self.tag_python = Tag.objects.create(name='python', slug='python')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')
        # 포스트 데이터 생성
        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
            category=self.category_programming, # 카테고리 추가
            author=self.user_trump,  
        )
        self.post_001.tags.add(self.tag_hello) # 태그 연결(ManyToManyField)

        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            category=self.category_music, # 카테고리 추가
            author=self.user_obama  
        )
        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='category가 없을 수도 있죠.',
            author=self.user_obama
        )
        self.post_003.tags.add(self.tag_python_kor) # 태그 연결(ManyToManyField)
        self.post_003.tags.add(self.tag_python)


    # 네비게이션 바 점검 -> 모듈 테스트를 위한 함수X(네이밍 컨벤션)
    # test_post_list()와 test_post_detail()에서 파싱된 HTML 요소를 받아서 테스트하기 위해 soup을 매개변수로 받음!
    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # 버튼 클릭 시 제대로 된 링크로 연결되는지 확인
        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    # 카테고리 점검
    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)


    # 포스트 목록 테스트 전면 수정(포스트가 있는 경우 vs 포스트가 없는 경우)
    def test_post_list(self):
        # 포스트가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup) # 네비게이션 바 점검
        self.category_card_test(soup) # 카테고리 점검

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)
        # 태그 테스트
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertIn(self.post_002.author.username.upper(), post_002_card.text)
        # 태그 테스트
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_003.author.username.upper(), post_003_card.text)
        # 태그 테스트
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)

        # self.assertIn(self.user_trump.username.upper(), main_area.text)
        # self.assertIn(self.user_obama.username.upper(), main_area.text)

        # 포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

    # 포스트 상세 페이지 테스트
    def test_post_detail(self):

        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.post_001.content, post_area.text)
        # 상세 페이지 태그 테스트(post_001에 대해서)
        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)

    # 카테고리 페이지 테스트 함수
    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        # 페이지 상단에 카테고리 뱃지가 잘 나타나는지 확인(<h1>태그)
        self.assertIn(self.category_programming.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        # post_002, 003의 제목은 메인영역에 존재하지 않는지 체크
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    # 태그 페이지 테스트
    def test_tag_page(self):
        # 1. setUp() 함수에서 만든 태그 중 name 필드가 'hello'인 것을 가져와서 테스트
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # 2.내비게이션 바와 오른쪽의 카테고리 카드를 테스트하는 navbar_test()와 category_card_test() 함수 재사용
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        # 3. 태그 페이지 제목(<h1\>)에 태그 이름이 있는지 확인
        self.assertIn(self.tag_hello.name, soup.h1.text)

        # 4. 메인 영역에 'hello'가 존재하는지 확인
        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)

        # 5. 이 태그가 붙어있는 self.post_001의 타이틀이 메인 영역에 존재하는지 확인
        self.assertIn(self.post_001.title, main_area.text)
        # 6. 'hello' 태그를 사용하지 않는 self.post_002와 self.post_003의 타이틀이 메인 영역에 없는지 확인
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    # 포스트 작성 페이지 테스트
    def test_create_post(self):

        # 로그인하지 않으면 status code가 200이 되면 안 됨!
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # trump(일반유저)로 로그인하여 테스트
        self.client.login(username='trump', password='somepassword')
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # obama(스태프)로 로그인하여 테스트
        self.client.login(username='obama', password='somepassword')
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)

        # submit 버튼 테스트
        self.client.post(
            '/blog/create_post/',
            {
                'title' : 'Post Form 만들기',
                'content' : 'Post Form 페이지를 만듭시다.',
            }
        )
        self.assertEqual(Post.objects.count(), 4)
        last_post = Post.objects.last()
        self.assertEqual(last_post.title, "Post Form 만들기")
        self.assertEqual(last_post.author.username, 'obama')

    # 포스트 수정 페이지 테스트
    def test_update_post(self):
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'

        # case1: 로그인 하지 않은 경우
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)
        
        # case2: 로그인은 했지만 작성자가 아닌 경우
        self.assertNotEqual(self.post_003.author, self.user_trump)
        self.client.login(
            username = self.user_trump.username,
            password = 'somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)
        
        # case3: 작성자(obama)가 접근하는 경우
        self.client.login(
            username = self.post_003.author.username,
            password = 'somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 페이지가 제대로 되어 있는지 확인
        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)

        # 수정사항이 제대로 반영 되는지 테스트
        response = self.client.post(
            update_post_url,
            {
                'title' : '세 번째 포스트를 수정했습니다.',
                'content' : '안녕 세계? 우리는 하나!',
                'category' : self.category_music.pk
            },
            follow = True
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('세 번째 포스트를 수정했습니다.', main_area.text)
        self.assertIn('안녕 세계? 우리는 하나!', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)






