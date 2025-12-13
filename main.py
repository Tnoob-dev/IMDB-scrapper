from requests.sessions import Session
from requests.exceptions import ConnectionError, ConnectTimeout
from bs4 import BeautifulSoup
from yarl import URL
from typing import NamedTuple, List

class ResultReturned(NamedTuple):
    name: str
    url: URL

class IMDB:
    def __init__(self, spanish: bool = True):
        self.url = "https://www.imdb.com/es-es" if spanish else "https://www.imdb.com"
        self.session = Session()
        self.user_agent = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0"}

    def search(self, query: str) -> List[ResultReturned]:
        
        try:
            
            response = self.session.get(self.url + f"/find/?q={query}", headers=self.user_agent, timeout=25)
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            if not (container := soup.find("div", attrs={"class": "sc-fe356c3c-2 hvzLGS"})):
                raise RuntimeError("El div principal de resultados no se encontro, o no existe")
            
            if not (results := container.find_all_next("a", attrs={"class": "ipc-title-link-wrapper", "tabindex": "0"})):
                return []
            
            new_links = [ResultReturned(res.text, URL(self.url + '/'.join(res.get("href").split("/")[2:]))) for res in results]
            
            return new_links
                    
        except (ConnectionError, ConnectTimeout) as error:
            raise RuntimeError(f"Error de conexion: {error}")
        
        except Exception as e:
            raise Exception(f"Error inesperado: {e}")
        
        finally:
            self.session.close()
        
    def get_info(self, url: URL):
        
        try:
            response = self.session.get(url, headers=self.user_agent, timeout=25)
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            print(soup.find("section", attrs={"class": "ipc-page-section ipc-page-section--baseAlt ipc-page-section--tp-none ipc-page-section--bp-xs sc-14a487d5-2 kmEeUD"}))
        
        except (ConnectionError, ConnectTimeout) as error:
            raise RuntimeError(f"Error de conexion: {error}")
        
        except Exception as e:
            raise Exception(f"Error inesperado: {e}")
        
        finally:
            self.session.close()
        
        
        
    

def main():
    
    url = "https://www.imdb.com/es-es"
    
    i = IMDB()
    
    result = i.search("Avatar")
    
    print(result)
    
    
    


if __name__ == "__main__":
    main()