class Spread:
    def __init__(self, key, name, card_count, positions):
        self.key = key
        self.name = name
        self.card_count = card_count
        self.positions = positions  # List of position names/meanings

# Single Card
single_spread = Spread(
    key="single",
    name="單張牌 (Single Card)",
    card_count=1,
    positions=["指引"]
)

# Time Flow
time_flow_spread = Spread(
    key="time_flow",
    name="時間之流 (Time Flow)",
    card_count=3,
    positions=["過去", "現在", "未來"]
)

# Four Elements
four_elements_spread = Spread(
    key="four_elements",
    name="四要素 (Four Elements)",
    card_count=4,
    positions=["火 (行動)", "水 (情感)", "風 (思考)", "土 (物質)"]
)

SPREADS = {
    "single": single_spread,
    "time_flow": time_flow_spread,
    "four_elements": four_elements_spread
}
