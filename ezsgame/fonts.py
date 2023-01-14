import pygame as pg, os

FONTS_PATH = "ezsgame/assets/fonts"

class FontFamily:
    def __init__(self, folder_name:str, main_font:str, is_variation:bool = False):
        
        """
        if is_variation is True then main_font is the file name of the font, not just the name of the font
        """
        # is variation font
        if is_variation:
            self.font_file = f"{FONTS_PATH}/{folder_name}/{main_font}"
        
        
        # if font family  get main font and variations
        else:

            # get variations                
            for filename in os.listdir(FONTS_PATH + "/" + folder_name):
                
                if filename.endswith(".ttf"):
                    
                    font_name = filename.replace(f"{folder_name}-", "")
                    font_name = font_name.replace(".ttf", "")
                    
                     # set main font
                    if font_name == main_font:
                        self.font_file = f"{FONTS_PATH}/{folder_name}/{filename}"
                        continue            

                    # set variations
                    setattr(self, font_name.lower(), FontFamily(folder_name, filename, True))
            
    def get_font(self, font_size) -> pg.font.Font:
        return pg.font.Font(self.font_file, font_size)
    

# default fonts  
class Fonts:
    RobotoMono: FontFamily = FontFamily("RobotoMono", "Regular")
    OpenSans = FontFamily("OpenSans", "Regular")