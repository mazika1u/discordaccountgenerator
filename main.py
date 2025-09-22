import random
import string
import requests
import json
import time
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor

class DiscordAccountCreator:
    def __init__(self):
        self.proxies = []
        self.password = "DefaultPassword123!"
        self.accounts_created = 0
        self.session = requests.Session()
        
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        ]
        
        self.domains = [
            "gmail.com", "yahoo.com", "hotmail.com", "outlook.com"
        ]
        
        self.load_config()
    
    def load_config(self):
        """設定ファイルの読み込み"""
        try:

            with open('proxy.txt', 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            print(f"[INFO] {len(self.proxies)}個のプロキシを読み込みました")
        except FileNotFoundError:
            print("[WARNING] proxy.txtが見つかりません。直接接続します")
        
        try:
          
            with open('pass.txt', 'r') as f:
                password = f.read().strip()
                if password:
                    self.password = password
            print(f"[INFO] パスワードを設定しました: {self.password}")
        except FileNotFoundError:
            print("[WARNING] pass.txtが見つかりません。デフォルトパスワードを使用します")
    
    def generate_random_username(self, length=6):
        """ランダムなユーザー名を生成"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def generate_email(self, username, domain_index=0):
        """メールアドレスを生成"""
        if domain_index < len(self.domains):
            return f"{username}@{self.domains[domain_index]}"
        return f"{username}@gmail.com"  # フォールバック
    
    def get_random_user_agent(self):
        """ランダムなユーザーエージェントを取得"""
        return random.choice(self.user_agents)
    
    def get_proxy(self):
        """ランダムなプロキシを取得（存在する場合）"""
        if self.proxies:
            proxy_str = random.choice(self.proxies)
            if '://' in proxy_str:
                return {'http': proxy_str, 'https': proxy_str}
            else:
                return {'http': f'http://{proxy_str}', 'https': f'https://{proxy_str}'}
        return None
    
    def check_domain_availability(self, domain):
        """ドメインの可用性をチェック（簡易版）"""
        return True
    
    def create_account(self, attempt_count=0):
        """Discordアカウントを作成"""
        username = self.generate_random_username()
        domain_index = attempt_count % len(self.domains)
        email = self.generate_email(username, domain_index)
        
        domain = self.domains[domain_index]
        if not self.check_domain_availability(domain):
            print(f"[WARNING] ドメイン {domain} は利用できません。次のドメインを試します")
            return self.create_account(attempt_count + 1)
        
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/register'
        }
        
        payload = {
            'email': email,
            'username': username,
            'password': self.password,
            'consent': True,
            'date_of_birth': self.generate_random_birthdate(),
            'fingerprint': None,
            'invite': None,
            'gift_code_sku_id': None
        }
        
        proxy = self.get_proxy()
        
        try:

            url = "https://discord.com/api/v9/auth/register"
            
            response = self.session.post(
                url,
                json=payload,
                headers=headers,
                proxies=proxy,
                timeout=30
            )
            
            if response.status_code == 201:
                self.accounts_created += 1
                account_data = {
                    'email': email,
                    'username': username,
                    'password': self.password,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                self.save_account(account_data)
                
                print(f"[SUCCESS] アカウント作成成功: {email}")
                return True
            else:
                print(f"[ERROR] アカウント作成失敗: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"[ERROR] 接続エラー: {str(e)}")
            return False
    
    def generate_random_birthdate(self):
        """ランダムな生年月日を生成（18歳以上）"""
        current_year = datetime.now().year
        year = random.randint(current_year - 40, current_year - 18)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # 簡単のため28日まで
        return f"{year}-{month:02d}-{day:02d}"
    
    def save_account(self, account_data):
        """アカウント情報をファイルに保存"""
        filename = f"accounts_{datetime.now().strftime('%Y%m%d')}.txt"
        
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"Email: {account_data['email']}\n")
            f.write(f"Username: {account_data['username']}\n")
            f.write(f"Password: {account_data['password']}\n")
            f.write(f"Created: {account_data['created_at']}\n")
            f.write("-" * 50 + "\n")
    
    def create_multiple_accounts(self, count=1, threads=1):
        """複数のアカウントを作成"""
        print(f"[INFO] {count}個のアカウント作成を開始します...")
        
        if threads > 1:
            with ThreadPoolExecutor(max_workers=threads) as executor:
                results = list(executor.map(lambda x: self.create_account(), range(count)))
        else:
            for i in range(count):
                self.create_account()

                time.sleep(random.uniform(2, 5))
        
        print(f"[INFO] アカウント作成完了: {self.accounts_created}/{count} 成功")

def main():
    """メイン関数"""
    print("=== Discordアカウント自動作成tool===")
    print("警告: このtoolはdiscordの規約違反です。自己責任")
    
    creator = DiscordAccountCreator()
    
    try:
        count = int(input("作成するアカウント数: "))
        threads = int(input("スレッド数 (推奨: 1-3): "))
        
        if count <= 0 or threads <= 0:
            print("無効な入力です")
            return
        
        creator.create_multiple_accounts(count, threads)
        
    except ValueError:
        print("数値を入力してください")
    except KeyboardInterrupt:
        print("\nプログラムを終了します")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()
