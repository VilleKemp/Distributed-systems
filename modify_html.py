from bs4 import BeautifulSoup


if __name__=="__main__":
    soup = BeautifulSoup(open("game.html"),"html.parser")
    script=soup.find_all('script')
    print script[1].string
    
    
    script[1].string.replaceWith("broken")
    print script[1]
    
