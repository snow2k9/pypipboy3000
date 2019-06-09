import pygame
from datetime import datetime
from random import randint

class menu(object):
  def __init__(self, display, displaySize, color, CONF):
      CONF["player"]["hp"] = randint(0,CONF["player"]["max_hp"])
      CONF["player"]["ap"] = randint(0,CONF["player"]["max_ap"])
      CONF["player"]["weight"] = randint(10,CONF["player"]["max_weight"])
      CONF["player"]["money"] = randint(152,CONF["player"]["money"])
      CONF["player"]["level"] = randint(0,100)
      CONF["player"]["level_progress"] = randint(0,100)

      self.display = display
      self.textColor = CONF["color"]
      self.inactiveTextColor = CONF["inactive_color"]
      self.boxColor = CONF["box_color"]

      self.menu = ["STAT", "INV", "DATA", "MAP", "RADIO"]
      self.submenu = {
        "STAT": ["STATUS", "SPECIAL", "PERKS"],
        "INV": ["WEAPONS", "APPAREL", "AID"],
        "DATA": ["QUESTS", "WORKSHOPS", "STATISTICS"],
        "MAP": [],
        "RADIO": []
      }

      self.min_width  = displaySize[0]/100
      self.max_width  = displaySize[0]/100 * 99
      self.min_height = displaySize[1]/100
      self.max_height = displaySize[1]/100 * 95
      self.text_start = self.min_width * 6
      self.text_end = self.min_width * 94

      self.margin  = (self.min_width * 2)
      self.margin_bottom  = (self.max_height - 2 * self.min_height)

      self.font = pygame.font.Font(CONF["font"], int(self.min_height * 5))
      self.small_font = pygame.font.Font(CONF["font"], int(self.min_height * 4))

      self.player = CONF["player"]

      #footer box structures
      # 25 - 25 - 50
      # self.footer_structure = {
      #   "left": [self.margin,self.margin_bottom, self.min_width * 25, self.small_font.get_height()],
      #   "center": [self.margin + 24 * self.min_width, self.margin_bottom, self.min_width * 25, self.small_font.get_height()],
      #   "right":  [self.margin + 49 * self.min_width, self.margin_bottom, self.min_width * 50, self.small_font.get_height()]
      # }

      # 25 - 50 - 25
      self.footer_structure = [{
        "left":   [self.margin, self.margin_bottom, self.min_width * 24.5, self.small_font.get_height()],
        "center": [self.margin + 25 * self.min_width, self.margin_bottom, self.min_width * 24.5, self.small_font.get_height()],
        "right":  [self.margin + 50 * self.min_width, self.margin_bottom, self.min_width * 49.5 - self.margin, self.small_font.get_height()]
        },
        {
        "left":   [self.margin, self.margin_bottom, self.min_width * 24.5, self.small_font.get_height()],
        "center": [self.margin + 25 * self.min_width, self.margin_bottom, self.min_width * 49.5 , self.small_font.get_height()],
        "right":  [self.margin + 75 * self.min_width, self.margin_bottom, self.min_width * 24.5 - self.margin, self.small_font.get_height()]
      }]

      if CONF["debug"]:
        print(self.player)

  def render_footer_text(self, text, position, struc):
    pygame.draw.rect(self.display, self.boxColor, self.footer_structure[struc][position])
    # set text right
    if position == "right":
      self.display.blit(text, ((self.footer_structure[struc][position][0] + self.footer_structure[struc][position][2] - text.get_width() - 5), self.margin_bottom))
    else:
      self.display.blit(text, (self.footer_structure[struc][position][0] + 5, self.margin_bottom))

  def render_footer(self, active_menu):
    texts = []
    struc = 0
    if active_menu == "STAT":
      struc = 1
      # HP
      texts.append([
        self.small_font.render(("I %(hp)i/%(max_hp)i" % {"hp": self.player["hp"], "max_hp": self.player["max_hp"]}), True, self.textColor),
        "left"
        ])

      # LEVEL AND Progress
      texts.append([
        self.small_font.render(("LEVEL %(level)i" % {"level": self.player["level"]}), True, self.textColor),
        "center"
        ])
      progress_pos_x1 = self.footer_structure[1]["center"][0] + texts[1][0].get_width() + self.min_width
      progress_pos_x2 = progress_pos_x1 + self.player["level_progress"] * (self.footer_structure[1]["center"][2] - texts[1][0].get_width())/100
      progress_pos_y = self.footer_structure[1]["center"][1] + texts[1][0].get_height()/2

      # AP
      texts.append([
        self.small_font.render(("I %(ap)i/%(max_ap)i" % {"ap": self.player["ap"], "max_ap": self.player["max_ap"]}), True, self.textColor),
        "right"
        ])

    if active_menu == "DATA":
      fallout_year = datetime.now()
      struc = 0
      # HP
      texts.append([
        self.small_font.render(("%(date)s" % { "date": fallout_year.strftime("%m.%d.2287") }), True, self.textColor),
        "left"
        ])

      # LEVEL AND Progress
      texts.append([
        self.small_font.render(("%(date)s" % { "date": fallout_year.strftime("%I:%M%p") }), True, self.textColor),
        "center"
        ])

      # AP
      texts.append([
        self.small_font.render("" , True, self.textColor),
        "right"
        ])

    if active_menu == "INV":
      struc = 0
      # weight box
      texts.append([
        self.small_font.render(("I %(weight)i/%(max_weight)i" % {"weight": self.player["weight"], "max_weight": self.player["max_weight"]}), True, self.textColor),
        "left"
        ])

      # money box
      texts.append([
        self.small_font.render(("I %(money)i" % {"money": self.player["money"]}), True, self.textColor),
        "center"
        ])

      # item stats TODO
      texts.append([
        self.small_font.render(("I %(weight)i/%(max_weight)i" % {"weight": self.player["weight"], "max_weight": self.player["max_weight"]}), True, self.textColor),
        "right"
        ])

    # render boxes and text
    for text in texts:
      self.render_footer_text(text[0], text[1], struc)
    if active_menu == "STAT":
      # render progress line
      pygame.draw.line(self.display, self.textColor,(progress_pos_x1, progress_pos_y),(progress_pos_x2, progress_pos_y), int(texts[1][0].get_height()/2))

  def render_submenu(self,menu,submenu, selected = 0):
    if menu == "DATA" and submenu == "QUESTS":
      self.render_quests(selected)

  def render_quests(self, selected = 0):
    quests = [
      ["The First Step", False, "Talk to the settlers at Tenpines"],
      ["Jewel of the Commonwealth", False, "Long teeeeextt"],
      ["Out of Time", True, "Not done yet!"]
    ]

    # Beginn of details
    current_height = self.min_height * 13

    quests_done = []
    quests_not_done = []
    for quest in quests:
      if quest[1]:
        color = self.inactiveTextColor
      else:
        color = self.textColor
      text = self.small_font.render(quest[0], True, color)
      if quest[1]:
        quests_done.append(text)
      else:
        quests_not_done.append(text)

    for i, quest in enumerate(quests_not_done):

      if i == selected:
        pygame.draw.rect(self.display, self.boxColor, [self.margin, current_height, self.max_width/2, self.small_font.get_height()])
      self.display.blit(quest, (self.margin * 2, current_height))
      current_height += quest.get_height()

    # current_height -= self.font.get_height()/2
    current_height += self.small_font.get_height()/2
    pygame.draw.aaline(self.display, self.textColor, (self.margin, current_height), (self.max_width/2,current_height))
    current_height += self.small_font.get_height()/8


    for i,quest in enumerate(quests_done):
      i += len(quests_not_done)
      if i == selected:
        pygame.draw.rect(self.display, self.boxColor, [self.margin, current_height, self.max_width/2, self.small_font.get_height()])
      self.display.blit(quest, (self.margin * 2, current_height))
      current_height += quest.get_height()

    # self.displaySize/2


  def update(self, SELECTION):
    #######
    # get active menu from selection
    active_menu = self.menu[SELECTION["menu_wheel"]]
    if self.submenu[active_menu]:
      active_submenu = self.submenu[active_menu][SELECTION["submenu_wheel"]]
    else:
      active_submenu = {}

    # print(active_menu)
    # print(active_submenu)

    #######
    # render footer
    self.render_footer(active_menu)

    #######
    # generate menu names
    menu_tabs = []
    for i, tab in enumerate(self.menu):
      if i == SELECTION["menu_wheel"]:
        color = self.textColor
      else:
        color = self.inactiveTextColor
      text = self.font.render(tab, True, color)
      menu_tabs.append([text])

    #######
    # generate submenu name from active_menu
    submenu_tabs = []
    for i, tab in enumerate(self.submenu[active_menu]):
      if i == SELECTION["submenu_wheel"]:
        color = self.textColor
      else:
        color = self.inactiveTextColor
      text = self.small_font.render(tab, True, color)
      submenu_tabs.append([text])

    #######
    # render menu
    menu_tab_width  = self.min_width * 100/len(self.menu) / 1.5
    menu_margin_left = self.max_width / 6
    submenu_pos = []
    for i, surface in enumerate(menu_tabs):
      start_pos = menu_margin_left + menu_tab_width * i
      submenu_pos.append(start_pos)
      self.display.blit(surface[0], (start_pos, self.min_height))

    #######
    #render submenu
    for i, surface in enumerate(submenu_tabs):
      start_pos = (submenu_pos[SELECTION["menu_wheel"]] + menu_tab_width * i) - (menu_tab_width * SELECTION["submenu_wheel"] - 1)
      self.display.blit(surface[0], (start_pos, self.min_height * 6))

    self.render_submenu(active_menu,active_submenu, SELECTION["selector"])
