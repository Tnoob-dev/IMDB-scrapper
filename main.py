from src.typo import ResultReturned, FinalResult
from src.exceptions import TagNotFound
from requests.sessions import Session
from requests.exceptions import ConnectionError, ConnectTimeout
from bs4 import BeautifulSoup, Tag
from yarl import URL
from typing import List, Tuple

class IMDB:
    def __init__(self):
        self.url = "https://www.imdb.com/es-es"
        self.session = Session()
        self.user_agent = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0"}

    def search(self, query: str) -> List[ResultReturned]:
        
        try:
            
            response = self.session.get(self.url + f"/find/?q={query}", headers=self.user_agent, timeout=25)
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            if not (container := soup.find("div", attrs={"class": "sc-fe356c3c-2 hvzLGS"})):
                raise TagNotFound(container.name)
            
            if not (results := container.find_all_next("a", attrs={"class": "ipc-title-link-wrapper", "tabindex": "0"})):
                return []
            
            new_links = [
                ResultReturned(
                    name=res.text, 
                    url=URL(
                        f"{self.url}/{'/'.join(res.get("href").split("/")[2:])}"
                        )
                    ) 
                for res in results]
            
            return new_links
                    
        except (ConnectionError, ConnectTimeout) as error:
            raise RuntimeError(f"Error de conexion: {error}")
        
        except Exception as error:
            raise RuntimeError(f"Error inesperado: {error}")
        
        except TagNotFound as error:
            raise error
    
    @staticmethod
    def _get_first_info_div(main_section: Tag) -> Tag:
        if not (div := main_section.find_next("div", attrs={"class": "sc-af040695-0 iOwuHP"})):
            raise TagNotFound("div.sc-af040695-0 iOwuHP")
        
        return div
    
    @staticmethod
    def _get_second_info_div(main_section: Tag) -> Tag:
        if not (div := main_section.find_next("div", attrs={"class": "sc-14a487d5-11 gFSFjL"})):
            raise TagNotFound("div.sc-14a487d5-11 gFSFjL")
        
        return div
    
    @staticmethod
    def _titles(main_section: Tag) -> Tuple[str, str]:
        
        try:
            div = IMDB._get_first_info_div(main_section)
            
            if not (title := div.find_next("h1", attrs={"data-testid": "hero__pageTitle"})):
                raise TagNotFound("h1")
            
            if not (org_title := div.find_next("div", {"class": "sc-b41e510f-2 jUfqFl baseAlt"})):
                org_title = title.text
            else:
                separated_org_title = org_title.text.split(" ")
                
                if len(separated_org_title) >= 2 and (separated_org_title[0] == "Título") and (separated_org_title[1] == "original:"):
                    for _ in range(2):
                        separated_org_title.pop(0)
                    
                    org_title = ' '.join(separated_org_title)
                
            return title.text, org_title
        
        except AttributeError as error:
            raise TagNotFound(f"Tag no encontrado: {error}")
        
    @staticmethod
    def _episode_duration(main_section: Tag) -> str:
        try:
            div = IMDB._get_first_info_div(main_section)

            if not (duration := div.find_next("ul", attrs={"role": "presentation"})):
                raise TagNotFound(duration.name)
            
            ep_duration = duration.find_all("li")[-1]
        
            return ep_duration.text
        except AttributeError as error:
            raise TagNotFound(f"Tag no encontrado: {error}")
        
    @staticmethod
    def _synopsis(main_section: Tag) -> str:
        try:
            div = IMDB._get_second_info_div(main_section)
            
            if not (p_tag := div.find_next("p", attrs={"class": "sc-bf30a0e-3 uWiw sc-bf30a0e-4 dKgygM"})):
                raise TagNotFound("p.sc-bf30a0e-3 uWiw sc-bf30a0e-4 dKgygM")
            
            if not (description := p_tag.find_next("span")):
                raise TagNotFound("span")
            
            return description.text
            
        except AttributeError as error:
            raise TagNotFound(f"Tag no encontrado: {error}")
    
    @staticmethod
    def _genres(main_section: Tag) -> List[str]:
        div = IMDB._get_second_info_div(main_section)
        
        if not (genre_scroller := div.find_next("div", attrs={"class": "ipc-chip-list__scroller"})):
            raise TagNotFound("div.ipc-chip-list__scroller")
        
        genres = genre_scroller.find_all_next("a", attrs={"class": "ipc-chip ipc-chip--on-baseAlt", "tabindex": "0", "aria-disabled": "false"})
    
        return [gen.text for gen in genres]
    
    def get_info(self, url: URL) -> FinalResult:
        
        try:
            response = self.session.get(url, headers=self.user_agent, timeout=25)
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            main_section = soup.find("section", attrs={"class": "ipc-page-section ipc-page-section--baseAlt ipc-page-section--tp-none ipc-page-section--bp-xs sc-14a487d5-2 kmEeUD"})
            
            title, original_title = IMDB._titles(main_section)
            duration = IMDB._episode_duration(main_section)
            
            synopsis = IMDB._synopsis(main_section)
            genres = IMDB._genres(main_section)
            
            return FinalResult(
                title=title,
                original_title=original_title,
                duration=duration,
                synopsis=synopsis,
                genres=genres
            )
            
        
        except (ConnectionError, ConnectTimeout) as error:
            raise RuntimeError(f"Error de conexion: {error}")
        
        except Exception as e:
            raise Exception(f"Error inesperado: {e}")
        
        finally:
            self.session.close()
    

def main():
    
    url = "https://www.imdb.com/es-es"
    
    i = IMDB()
    
    result = i.search("Avatar la leyenda de Aang")
    
    url = result[0].url
    print(i.get_info(url))

if __name__ == "__main__":
    main()