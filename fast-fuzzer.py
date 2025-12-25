import asyncio, aiohttp, time, sys, argparse
from colorama import init, Fore, Style

# تعطيل تحذيرات SSL المزعجة
import urllib3
urllib3.disable_warnings()

init(autoreset=True)

# ============================================================
# [1] ARGUMENTS & CONFIGURATION
# ============================================================
parser = argparse.ArgumentParser(description="Pro Fuzzer v1.0")
parser.add_argument('-m', '--mathed', type=str, required=True, help="Mode: dir or domin")
parser.add_argument('-u', '--url', type=str, required=True, help="Target URL")
parser.add_argument('-w', '--wordlist', type=str, required=True, help="Wordlist path")
parser.add_argument('-t', '--timeout', type=int, default=5)
parser.add_argument('-T', '--threads', type=int, default=50)
parser.add_argument('-x', '--extunions', nargs='*', default=[''])
parser.add_argument('-s', '--save', action='store_true', help="Save results")

args = parser.parse_args()

TARGET       = args.url
WORDLISTFILE = args.wordlist
MATHED       = args.mathed.lower()
THREDS       = args.threads
TIMEOUT      = args.timeout
EXTUNINOS    = args.extunions
SAVING       = args.save
FACKPAGE     = 1520
RESULTFILE   = 'FUZING_result.txt'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
}

counter = 0
total_words = 0

# ============================================================
# [2] UTILITIES
# ============================================================

def print_banner():
    banner = f"""
    {Fore.MAGENTA}=======================================
    {Fore.CYAN}      FAST-FUZZER - BY DKHEL-ALDOSRY
    {Fore.MAGENTA}=======================================
    {Fore.YELLOW} Target:  {TARGET}
    {Fore.YELLOW} threds:  {THREDS}
    {Fore.YELLOW} timeout: {TIMEOUT}
    {Fore.YELLOW} Mode:    {MATHED}
    {Fore.MAGENTA}---------------------------------------
    """
    print(banner)

def save_result(data):
    with open(RESULTFILE, 'a') as file:
        file.write(f'{data}\n')

def update_progress():
    sys.stdout.write(f'\r{Fore.WHITE}[@] Progress: ({counter}/{total_words})')
    sys.stdout.flush()

# 

# ============================================================
# [3] ENGINES
# ============================================================

async def dir_fuzzing(session, fullurl, semaphore):
    global counter
    async with semaphore:
        try:
            async with session.get(fullurl, timeout=TIMEOUT, allow_redirects=False) as response:
                status = response.status
                content = await response.read()
                size = len(content)

                # منطق تلوين الحالات
                color = Fore.WHITE
                if status == 200: color = Fore.GREEN
                elif status in [301, 302]: color = Fore.YELLOW
                elif status == 403: color = Fore.RED

                if status == 200 and size != FACKPAGE:
                    line = f'\r{color}[+] Found: {fullurl} (Status: {status}) (Size: {size})'
                    print(line.ljust(100))
                    if SAVING: save_result(line)
                elif status in [301, 302]:
                    loc = response.headers.get('Location', 'Unknown')
                    print(f'\r{color}[#] {status} Redirect: {fullurl} -> {loc}'.ljust(100))
        except:
            pass
        finally:
            counter += 1
            update_progress()

async def domin_fuzzing(session, word, semaphore, protocol, domain_part):
    global counter
    fullurl = f'{protocol}://{word}.{domain_part}'
    async with semaphore:
        try:
            async with session.get(fullurl, timeout=TIMEOUT, allow_redirects=False) as response:
                status = response.status
                if status == 200:
                    line = f'\r{Fore.GREEN}[+] Subdomain: {fullurl}'
                    print(line.ljust(100))
                    if SAVING: save_result(line)
        except:
            pass
        finally:
            counter += 1
            update_progress()

# ============================================================
# [4] MAIN CONTROLLER
# ============================================================

async def main():
    global total_words
    print_banner()

    if not TARGET.startswith(('http://', 'https://')):
        print(f"{Fore.RED}[!] Error: Target must start with http/https")
        return

    # معالجة الرابط النظيف
    clean_target = TARGET.rstrip('/')
    parts = clean_target.split('://')
    protocol = parts[0]
    domain_part = parts[1].split('/')[0]

    try:
        with open(WORDLISTFILE, 'r') as f:
            words = [l.strip() for l in f if l.strip()]
    except:
        print(f"{Fore.RED}[!] Wordlist not found.")
        return

    semaphore = asyncio.Semaphore(THREDS)
    tasks = []

    # إعداد الجلسة مع تعطيل SSL verification
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(headers=HEADERS, connector=connector) as session:
        
        # تحسين: فحص الوضع خارج الحلقة لزيادة السرعة
        if MATHED == 'dir':
            for word in words:
                for ext in EXTUNINOS:
                    url = f"{clean_target}/{word}{ext}"
                    tasks.append(dir_fuzzing(session, url, semaphore))
        elif MATHED == 'domin':
            for word in words:
                tasks.append(domin_fuzzing(session, word, semaphore, protocol, domain_part))
        else:
            print(f"{Fore.RED}[!] Invalid mode. Use 'dir' or 'domin'.")
            return

        total_words = len(tasks)
        if tasks:
            start_time = time.time()
            await asyncio.gather(*tasks)
            print(f"\n\n{Fore.MAGENTA}[*] Finished in {time.time() - start_time:.2f}s")
def main_entry():
    """هذه هي الدالة التي سيقوم نظام التشغيل باستدعائها"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Aborted by user.")
        sys.exit()

if __name__ == '__main__':
    main_entry()
