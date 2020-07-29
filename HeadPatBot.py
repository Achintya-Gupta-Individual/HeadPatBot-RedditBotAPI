import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
USERNAME  = "HeadPatBot"
PASSWORD  = "achintya19"
USER_AGENT = "HeadPatBot by /u/LordOfEnnui"
CLIENT_SECRET = "22pazgj-Zbfa2HsdlJXv9YYNqfY"
CLIENT_ID = "PfRQJemRJ2ni1Q"
SUBREDDIT = "wholesomeanimemes+test"
KEYSTRING = "!headpat"
REPLY = "There There... Have a headpat"
RATELIMIT = 1 #10*60
TIMEINTERVAL = 1


comment_authors = {}
comments_done = []
comments_made = []
replies_handled = {
    "good bot" : "[thank you (*^.^*)](https://cutewallpaper.org/21/kono-subarashii-sekai-ni-shukufuku-wo-wallpaper/Kono-Subarashii-Sekai-ni-Shukufuku-wo-Wallpaper-2605849-.jpg)",
    "bad bot" : "[I will have my vengeance](https://pics.me.me/thumb_he-has-come-for-us-all-and-he-seeks-vengeance-68478577.png)",
    "I don't want your headpats" : "[:(](https://pics.me.me/thumb_he-has-come-for-us-all-and-he-seeks-vengeance-68478577.png)",
    "thank you" : "It's not like I l-like you or anything!"
}
#r_pat = re.compile(' r/[A-Za-z0-9]+')
#u_pat = re.compile(' u/[A-Za-z0-9]+')

def main():
    try:
        reddit = praw.Reddit(user_agent=USERNAME,
                    client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                    username=USERNAME, password=PASSWORD)
        subreddit = reddit.subreddit(SUBREDDIT)  
        running = True
        comments = subreddit.stream.comments(skip_existing = True)

        while running:
            #time.sleep(TIMEINTERVAL)
            print("looping")
            for comment in comments:
                print(comment.parent_id)
                author = comment.author.name
                if author in comment_authors:
                    if time.process_time() - comment_authors[author] > 60*60:
                        comment_authors.pop(author)
                        print("duplicate" + comment.body)
                invalid = author in comment_authors or comment.id in comments_done
                if KEYSTRING in comment.body and not invalid:
                    print("headpat")
                    reply_made = comment.reply(REPLY)
                    #comment_authors[author] = time.process_time()
                    comments_done.append(comment.id)
                    #print("waiting to continue")
                    #time.sleep(RATELIMIT)
                    #print("wait over")
                    print("t1_" + reply_made.id)
                    comments_made.append("t1_" + reply_made.id)

                if comment.parent_id in comments_made:
                    for reply in replies_handled:
                        if reply in comment.body:
                            comment.reply(replies_handled[reply])
                            print(reply)
                            break

    except KeyboardInterrupt as e:
        print("[Breakout]", e)
    except praw.exceptions.RedditAPIException as e:
        print("[ERROR]", e)
    except Exception as e:
        print("[Problem]", e)
        
main()