import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
USERNAME  = "HeadPatBot"
PASSWORD  = "Arock19&"
USER_AGENT = "HeadPatBot by /u/LordOfEnnui"
CLIENT_SECRET = "22pazgj-Zbfa2HsdlJXv9YYNqfY"
CLIENT_ID = "PfRQJemRJ2ni1Q"
SUBREDDIT = "wholesomeanimemes+test"
KEYSTRING = "!headpat"
REPLY = "There There... Have a headpat\n\n[BETA] I'm a bot, please help me test\n\nSadly, I can only headpat once every 10 minutes"
RATELIMIT = 10*60
TIMEINTERVAL = 1


comment_authors = {}
comments_done = []

#r_pat = re.compile(' r/[A-Za-z0-9]+')
#u_pat = re.compile(' u/[A-Za-z0-9]+')

def main():
    reddit = praw.Reddit(user_agent=USERNAME,
                client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                username=USERNAME, password=PASSWORD)
    subreddit = reddit.subreddit(SUBREDDIT)
    
    running = True
    comments = subreddit.stream.comments(skip_existing = True)
    while running:
        try:
            #time.sleep(TIMEINTERVAL)
            print("looping")
            for comment in comments:
                print(comment.body)
                author = comment.author.name
                if  author in comment_authors:
                    if time.process_time() - comment_authors[author] > 60*60:
                        comment_authors.pop(author)
                        print("duplicate" + comment.body)
                invalid = author in comment_authors or comment.id in comments_done
                if KEYSTRING in comment.body and not invalid:
                    print("headpat")
                    comment.reply(REPLY)
                    #comment_authors[author] = time.process_time()
                    comments_done.append(comment.id)
                    print("waiting to continue")
                    time.sleep(RATELIMIT)
                    print("wait over")
        except KeyboardInterrupt as e:
            print("[Breakout]", e)
            running = False
            break
        except praw.exceptions.RedditAPIException as e:
            print("[ERROR]", e)
        except Exception as e:
            print("[Problem]", e)
        
main()