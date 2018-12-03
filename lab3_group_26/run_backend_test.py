import pprint
import crawler
import sqlite3
import time

GREENLIGHT_DB = "greenLight.db"
if __name__ == '__main__':
    bot = crawler.crawler(None, "urls.txt")
    bot.crawl(depth=1)
    bot._inverted_index = bot.get_inverted_index()
    bot._resolved_inverted_index = bot.get_resolved_inverted_index()

    t0=time.time()
    # check if the links are not empty
    if (bool(bot._links)):
        bot._pagerank_score = bot.get_pagerank_score()
    t1=time.time()
    print 'time is %.5f ' %(t1-t0)

    #store to persistent dateabase
    bot.initialize_persistent_database()
    bot.store_to_database()


    con = sqlite3.connect(GREENLIGHT_DB)
    cur = con.cursor()

    sorted_pagerank = list(cur.execute("SELECT * FROM PAGERANK_SCORE ORDER BY DOC_SCORE DESC"))
    pprint.pprint(sorted_pagerank)
    cur.close()
