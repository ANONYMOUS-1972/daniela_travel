# travel_iq_app.py — TravelIQ v2.0
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
import calendar
from typing import Dict, List, Any

# ------------------------------------------------------------------------------
# PAGE CONFIGURATION
st.set_page_config(
    layout="wide",
    page_title="TravelIQ — Smart Destination Analyzer",
    page_icon="✈️"
)

st.markdown("""
<style>
    .card {
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin: 0.8rem 0;
        background-color: #2d3250;
        border: 1px solid #4a5080;
        box-shadow: 0 4px 16px rgba(0,0,0,0.35);
        transition: transform 0.2s, background-color 0.2s;
    }
    .card:hover { transform: translateY(-4px); background-color: #363c6a; }
    .card h2 { color: #e8eeff !important; font-size: 1.1rem; margin: 0; line-height: 1.4; }
    .hotel-card {
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        background-color: #1e2540;
        border: 1px solid #3a4070;
    }
    .hotel-card h4 { color: #e8eeff !important; margin: 0 0 4px 0; font-size: 1rem; }
    .hotel-card p  { color: #a8b4d8 !important; margin: 2px 0; font-size: 0.85rem; }
    .badge-green  { background-color:#1a7a3c; color:#b6ffce; padding:0.2rem 0.65rem; border-radius:30px; font-size:0.78rem; display:inline-block; font-weight:600; }
    .badge-yellow { background-color:#7a6200; color:#ffe899; padding:0.2rem 0.65rem; border-radius:30px; font-size:0.78rem; display:inline-block; font-weight:600; }
    .badge-orange { background-color:#7a3400; color:#ffbd85; padding:0.2rem 0.65rem; border-radius:30px; font-size:0.78rem; display:inline-block; font-weight:600; }
    .badge-blue   { background-color:#0a3d7a; color:#a8d4ff; padding:0.2rem 0.65rem; border-radius:30px; font-size:0.78rem; display:inline-block; font-weight:600; }
    .badge-gold   { background-color:#5a4200; color:#ffd966; padding:0.2rem 0.65rem; border-radius:30px; font-size:0.78rem; display:inline-block; font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# DESTINATION DATABASE — enriched with country + tourist_spots
def load_destinations() -> List[Dict]:
    destinations = [
        # EUROPE
        {"destination":"Lisbon","country":"Portugal","continent":"Europe","tourist_spots":["Belém Tower","Alfama District","Jerónimos Monastery","Sintra","LX Factory"],"avg_flight_cost_eur":150,"avg_hotel_7nights_full_board":700,"avg_hotel_7nights_half_board":560,"local_daily_expenses_eur":45,"best_months":["March","April","May","September","October"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":8.7,"highlights":["Belém Tower","Tram 28 Ride","Pastéis de Belém"],"visa_required_for_italians":False,"currency":"EUR","language":"Portuguese","climate_in_best_months":"Mild and sunny","flag_emoji":"🇵🇹","lat":38.72,"lon":-9.14},
        {"destination":"Porto","country":"Portugal","continent":"Europe","tourist_spots":["Dom Luís I Bridge","Ribeira District","Port Wine Cellars","Livraria Lello","Bolhão Market"],"avg_flight_cost_eur":140,"avg_hotel_7nights_full_board":650,"avg_hotel_7nights_half_board":520,"local_daily_expenses_eur":40,"best_months":["May","June","September"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":8.9,"highlights":["Dom Luís I Bridge","Port Wine Cellars","Ribeira District"],"visa_required_for_italians":False,"currency":"EUR","language":"Portuguese","climate_in_best_months":"Warm and dry","flag_emoji":"🇵🇹","lat":41.15,"lon":-8.61},
        {"destination":"Barcelona","country":"Spain","continent":"Europe","tourist_spots":["Sagrada Familia","Park Güell","Gothic Quarter","La Boqueria","Camp Nou"],"avg_flight_cost_eur":120,"avg_hotel_7nights_full_board":800,"avg_hotel_7nights_half_board":640,"local_daily_expenses_eur":60,"best_months":["April","May","June","September","October"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":["Petty crime risk in crowded areas"],"value_score":8.2,"highlights":["Sagrada Familia","Park Güell","Las Ramblas"],"visa_required_for_italians":False,"currency":"EUR","language":"Spanish","climate_in_best_months":"Warm and pleasant","flag_emoji":"🇪🇸","lat":41.39,"lon":2.15},
        {"destination":"Madrid","country":"Spain","continent":"Europe","tourist_spots":["Prado Museum","Retiro Park","Royal Palace","Puerta del Sol","Mercado de San Miguel"],"avg_flight_cost_eur":130,"avg_hotel_7nights_full_board":780,"avg_hotel_7nights_half_board":620,"local_daily_expenses_eur":55,"best_months":["April","May","June","September","October"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":8.1,"highlights":["Prado Museum","Royal Palace","Retiro Park"],"visa_required_for_italians":False,"currency":"EUR","language":"Spanish","climate_in_best_months":"Mild and sunny","flag_emoji":"🇪🇸","lat":40.42,"lon":-3.70},
        {"destination":"Rome","country":"Italy","continent":"Europe","tourist_spots":["Colosseum","Vatican Museums","Trevi Fountain","Pantheon","Borghese Gallery"],"avg_flight_cost_eur":80,"avg_hotel_7nights_full_board":900,"avg_hotel_7nights_half_board":720,"local_daily_expenses_eur":65,"best_months":["April","May","June","September","October"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":7.9,"highlights":["Colosseum","Vatican City","Trevi Fountain"],"visa_required_for_italians":False,"currency":"EUR","language":"Italian","climate_in_best_months":"Warm and sunny","flag_emoji":"🇮🇹","lat":41.90,"lon":12.50},
        {"destination":"Florence","country":"Italy","continent":"Europe","tourist_spots":["Uffizi Gallery","Duomo","Ponte Vecchio","Boboli Gardens","Accademia Gallery"],"avg_flight_cost_eur":100,"avg_hotel_7nights_full_board":850,"avg_hotel_7nights_half_board":680,"local_daily_expenses_eur":60,"best_months":["April","May","June","September","October"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":8.3,"highlights":["Uffizi Gallery","Duomo","Ponte Vecchio"],"visa_required_for_italians":False,"currency":"EUR","language":"Italian","climate_in_best_months":"Mild and pleasant","flag_emoji":"🇮🇹","lat":43.77,"lon":11.25},
        {"destination":"Paris","country":"France","continent":"Europe","tourist_spots":["Eiffel Tower","Louvre","Notre-Dame","Montmartre","Versailles"],"avg_flight_cost_eur":110,"avg_hotel_7nights_full_board":1100,"avg_hotel_7nights_half_board":880,"local_daily_expenses_eur":80,"best_months":["April","May","June","September","October"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":["Strike disruptions possible"],"value_score":7.5,"highlights":["Eiffel Tower","Louvre","Notre-Dame"],"visa_required_for_italians":False,"currency":"EUR","language":"French","climate_in_best_months":"Mild and pleasant","flag_emoji":"🇫🇷","lat":48.86,"lon":2.35},
        {"destination":"Athens","country":"Greece","continent":"Europe","tourist_spots":["Acropolis","Parthenon","Plaka","National Archaeological Museum","Cape Sounion"],"avg_flight_cost_eur":180,"avg_hotel_7nights_full_board":750,"avg_hotel_7nights_half_board":600,"local_daily_expenses_eur":55,"best_months":["April","May","June","September","October"],"geopolitical_risk":"low","conflict_zone":False,"active_warnings":[],"value_score":8.0,"highlights":["Acropolis","Plaka","Temple of Olympian Zeus"],"visa_required_for_italians":False,"currency":"EUR","language":"Greek","climate_in_best_months":"Warm and dry","flag_emoji":"🇬🇷","lat":37.98,"lon":23.73},
        {"destination":"Budapest","country":"Hungary","continent":"Europe","tourist_spots":["Buda Castle","Parliament","Széchenyi Baths","Fisherman's Bastion","Ruin Bars"],"avg_flight_cost_eur":160,"avg_hotel_7nights_full_board":600,"avg_hotel_7nights_half_board":480,"local_daily_expenses_eur":45,"best_months":["April","May","June","September","October"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":9.0,"highlights":["Buda Castle","Parliament","Széchenyi Baths"],"visa_required_for_italians":False,"currency":"HUF","language":"Hungarian","climate_in_best_months":"Mild and sunny","flag_emoji":"🇭🇺","lat":47.50,"lon":19.04},
        {"destination":"Krakow","country":"Poland","continent":"Europe","tourist_spots":["Wawel Castle","Main Market Square","Auschwitz-Birkenau","Kazimierz District","Salt Mine Wieliczka"],"avg_flight_cost_eur":130,"avg_hotel_7nights_full_board":550,"avg_hotel_7nights_half_board":440,"local_daily_expenses_eur":40,"best_months":["May","June","July","August","September"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":9.2,"highlights":["Wawel Castle","Main Market Square","Auschwitz-Birkenau"],"visa_required_for_italians":False,"currency":"PLN","language":"Polish","climate_in_best_months":"Warm and pleasant","flag_emoji":"🇵🇱","lat":50.06,"lon":19.94},
        {"destination":"Reykjavik","country":"Iceland","continent":"Europe","tourist_spots":["Blue Lagoon","Golden Circle","Northern Lights","Hallgrímskirkja","Þingvellir National Park"],"avg_flight_cost_eur":250,"avg_hotel_7nights_full_board":1300,"avg_hotel_7nights_half_board":1040,"local_daily_expenses_eur":100,"best_months":["June","July","August","September"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":7.5,"highlights":["Northern Lights","Blue Lagoon","Golden Circle"],"visa_required_for_italians":False,"currency":"ISK","language":"Icelandic","climate_in_best_months":"Mild and bright nights","flag_emoji":"🇮🇸","lat":64.13,"lon":-21.94},
        # ASIA
        {"destination":"Tokyo","country":"Japan","continent":"Asia","tourist_spots":["Shibuya Crossing","Senso-ji Temple","Shinjuku","Akihabara","teamLab Borderless"],"avg_flight_cost_eur":1000,"avg_hotel_7nights_full_board":1400,"avg_hotel_7nights_half_board":1120,"local_daily_expenses_eur":70,"best_months":["March","April","October","November"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":8.4,"highlights":["Shibuya Crossing","Senso-ji Temple","Tokyo Tower"],"visa_required_for_italians":False,"currency":"JPY","language":"Japanese","climate_in_best_months":"Cherry blossoms or mild autumn","flag_emoji":"🇯🇵","lat":35.68,"lon":139.69},
        {"destination":"Kyoto","country":"Japan","continent":"Asia","tourist_spots":["Fushimi Inari","Kinkaku-ji","Arashiyama Bamboo","Gion District","Nijo Castle"],"avg_flight_cost_eur":1050,"avg_hotel_7nights_full_board":1350,"avg_hotel_7nights_half_board":1080,"local_daily_expenses_eur":65,"best_months":["March","April","October","November"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":8.6,"highlights":["Fushimi Inari","Kinkaku-ji","Arashiyama Bamboo"],"visa_required_for_italians":False,"currency":"JPY","language":"Japanese","climate_in_best_months":"Cherry blossoms or colorful leaves","flag_emoji":"🇯🇵","lat":35.01,"lon":135.77},
        {"destination":"Bangkok","country":"Thailand","continent":"Asia","tourist_spots":["Grand Palace","Wat Arun","Chatuchak Market","Khao San Road","Floating Markets"],"avg_flight_cost_eur":750,"avg_hotel_7nights_full_board":600,"avg_hotel_7nights_half_board":480,"local_daily_expenses_eur":35,"best_months":["November","December","January","February"],"geopolitical_risk":"low","conflict_zone":False,"active_warnings":["Occasional political protests"],"value_score":9.0,"highlights":["Grand Palace","Wat Arun","Chatuchak Market"],"visa_required_for_italians":False,"currency":"THB","language":"Thai","climate_in_best_months":"Cool and dry","flag_emoji":"🇹🇭","lat":13.75,"lon":100.52},
        {"destination":"Chiang Mai","country":"Thailand","continent":"Asia","tourist_spots":["Doi Suthep","Old City Temples","Night Bazaar","Elephant Sanctuaries","Doi Inthanon"],"avg_flight_cost_eur":800,"avg_hotel_7nights_full_board":500,"avg_hotel_7nights_half_board":400,"local_daily_expenses_eur":30,"best_months":["November","December","January","February"],"geopolitical_risk":"low","conflict_zone":False,"active_warnings":[],"value_score":9.3,"highlights":["Doi Suthep","Old City Temples","Night Bazaar"],"visa_required_for_italians":False,"currency":"THB","language":"Thai","climate_in_best_months":"Cool and pleasant","flag_emoji":"🇹🇭","lat":18.79,"lon":98.98},
        {"destination":"Bali","country":"Indonesia","continent":"Asia","tourist_spots":["Ubud Rice Terraces","Tanah Lot","Mount Batur","Uluwatu Temple","Seminyak Beach"],"avg_flight_cost_eur":900,"avg_hotel_7nights_full_board":800,"avg_hotel_7nights_half_board":640,"local_daily_expenses_eur":40,"best_months":["April","May","June","July","August","September"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":8.8,"highlights":["Ubud Rice Terraces","Tanah Lot","Mount Batur"],"visa_required_for_italians":False,"currency":"IDR","language":"Indonesian","climate_in_best_months":"Dry season","flag_emoji":"🇮🇩","lat":-8.34,"lon":115.09},
        {"destination":"Seoul","country":"South Korea","continent":"Asia","tourist_spots":["Gyeongbokgung Palace","N Seoul Tower","Myeongdong","Bukchon Hanok Village","DMZ Tour"],"avg_flight_cost_eur":850,"avg_hotel_7nights_full_board":1100,"avg_hotel_7nights_half_board":880,"local_daily_expenses_eur":60,"best_months":["April","May","September","October"],"geopolitical_risk":"low","conflict_zone":False,"active_warnings":[],"value_score":8.3,"highlights":["Gyeongbokgung Palace","N Seoul Tower","Myeongdong"],"visa_required_for_italians":False,"currency":"KRW","language":"Korean","climate_in_best_months":"Mild and sunny","flag_emoji":"🇰🇷","lat":37.57,"lon":126.98},
        {"destination":"Hanoi","country":"Vietnam","continent":"Asia","tourist_spots":["Hoan Kiem Lake","Old Quarter","Ho Chi Minh Mausoleum","Ha Long Bay","Temple of Literature"],"avg_flight_cost_eur":800,"avg_hotel_7nights_full_board":550,"avg_hotel_7nights_half_board":440,"local_daily_expenses_eur":30,"best_months":["October","November","December","January","February","March"],"geopolitical_risk":"low","conflict_zone":False,"active_warnings":[],"value_score":9.1,"highlights":["Hoan Kiem Lake","Old Quarter","Ha Long Bay day trip"],"visa_required_for_italians":False,"currency":"VND","language":"Vietnamese","climate_in_best_months":"Cool and dry","flag_emoji":"🇻🇳","lat":21.03,"lon":105.85},
        {"destination":"Hoi An","country":"Vietnam","continent":"Asia","tourist_spots":["Ancient Town","Japanese Bridge","An Bang Beach","My Son Sanctuary","Lantern Festival"],"avg_flight_cost_eur":820,"avg_hotel_7nights_full_board":480,"avg_hotel_7nights_half_board":380,"local_daily_expenses_eur":28,"best_months":["February","March","April","May","June","July","August"],"geopolitical_risk":"low","conflict_zone":False,"active_warnings":[],"value_score":9.5,"highlights":["Ancient Town","Japanese Bridge","Tailor Shops"],"visa_required_for_italians":False,"currency":"VND","language":"Vietnamese","climate_in_best_months":"Warm and dry","flag_emoji":"🇻🇳","lat":15.88,"lon":108.34},
        {"destination":"Siem Reap","country":"Cambodia","continent":"Asia","tourist_spots":["Angkor Wat","Angkor Thom","Ta Prohm","Tonle Sap Lake","Pub Street"],"avg_flight_cost_eur":850,"avg_hotel_7nights_full_board":500,"avg_hotel_7nights_half_board":400,"local_daily_expenses_eur":30,"best_months":["November","December","January","February","March"],"geopolitical_risk":"low","conflict_zone":False,"active_warnings":[],"value_score":9.4,"highlights":["Angkor Wat","Tonle Sap","Pub Street"],"visa_required_for_italians":True,"currency":"KHR","language":"Khmer","climate_in_best_months":"Cool and dry","flag_emoji":"🇰🇭","lat":13.36,"lon":103.86},
        # AFRICA
        {"destination":"Marrakech","country":"Morocco","continent":"Africa","tourist_spots":["Jemaa el-Fnaa","Bahia Palace","Majorelle Garden","Medina Souks","Atlas Mountains day trip"],"avg_flight_cost_eur":250,"avg_hotel_7nights_full_board":650,"avg_hotel_7nights_half_board":520,"local_daily_expenses_eur":40,"best_months":["March","April","May","September","October","November"],"geopolitical_risk":"low","conflict_zone":False,"active_warnings":[],"value_score":8.5,"highlights":["Jemaa el-Fnaa","Bahia Palace","Majorelle Garden"],"visa_required_for_italians":False,"currency":"MAD","language":"Arabic","climate_in_best_months":"Warm and sunny","flag_emoji":"🇲🇦","lat":31.63,"lon":-7.99},
        {"destination":"Cape Town","country":"South Africa","continent":"Africa","tourist_spots":["Table Mountain","Robben Island","Cape Winelands","Boulders Penguin Colony","Chapman's Peak"],"avg_flight_cost_eur":850,"avg_hotel_7nights_full_board":950,"avg_hotel_7nights_half_board":760,"local_daily_expenses_eur":55,"best_months":["November","December","January","February","March"],"geopolitical_risk":"medium","conflict_zone":False,"active_warnings":["Crime in certain areas"],"value_score":8.0,"highlights":["Table Mountain","Robben Island","Cape Winelands"],"visa_required_for_italians":False,"currency":"ZAR","language":"Afrikaans","climate_in_best_months":"Dry and warm","flag_emoji":"🇿🇦","lat":-33.93,"lon":18.42},
        {"destination":"Zanzibar","country":"Tanzania","continent":"Africa","tourist_spots":["Stone Town","Nakupenda Beach","Nungwi Beach","Spice Tour","Prison Island"],"avg_flight_cost_eur":750,"avg_hotel_7nights_full_board":1100,"avg_hotel_7nights_half_board":880,"local_daily_expenses_eur":50,"best_months":["June","July","August","September","October","December","January","February"],"geopolitical_risk":"low","conflict_zone":False,"active_warnings":[],"value_score":8.2,"highlights":["Stone Town","Nakupenda Beach","Spice Tour"],"visa_required_for_italians":True,"currency":"TZS","language":"Swahili","climate_in_best_months":"Dry and sunny","flag_emoji":"🇹🇿","lat":-6.16,"lon":39.20},
        {"destination":"Djerba","country":"Tunisia","continent":"Africa","tourist_spots":["Houmt Souk","El Ghriba Synagogue","Flamingo Beach","Guellala Museum","Crocodile Farm"],"avg_flight_cost_eur":220,"avg_hotel_7nights_full_board":600,"avg_hotel_7nights_half_board":480,"local_daily_expenses_eur":35,"best_months":["April","May","June","September","October"],"geopolitical_risk":"medium","conflict_zone":False,"active_warnings":["Occasional security alerts"],"value_score":8.7,"highlights":["Houmt Souk","El Ghriba Synagogue","Flamingo Beach"],"visa_required_for_italians":False,"currency":"TND","language":"Arabic","climate_in_best_months":"Warm and sunny","flag_emoji":"🇹🇳","lat":33.80,"lon":10.85},
        # AMERICAS
        {"destination":"Mexico City","country":"Mexico","continent":"Americas","tourist_spots":["Teotihuacan","Frida Kahlo Museum","Zócalo","Chapultepec Park","Xochimilco"],"avg_flight_cost_eur":800,"avg_hotel_7nights_full_board":700,"avg_hotel_7nights_half_board":560,"local_daily_expenses_eur":45,"best_months":["March","April","May","October","November"],"geopolitical_risk":"medium","conflict_zone":False,"active_warnings":["Petty crime, occasional protests"],"value_score":8.2,"highlights":["Teotihuacan","Frida Kahlo Museum","Zócalo"],"visa_required_for_italians":False,"currency":"MXN","language":"Spanish","climate_in_best_months":"Mild and dry","flag_emoji":"🇲🇽","lat":19.43,"lon":-99.13},
        {"destination":"Cancún","country":"Mexico","continent":"Americas","tourist_spots":["Chichen Itza","Tulum","Isla Mujeres","Xcaret Park","Cenotes"],"avg_flight_cost_eur":850,"avg_hotel_7nights_full_board":1200,"avg_hotel_7nights_half_board":960,"local_daily_expenses_eur":60,"best_months":["December","January","February","March","April"],"geopolitical_risk":"low","conflict_zone":False,"active_warnings":[],"value_score":8.0,"highlights":["Mayan Ruins","Beaches","Isla Mujeres"],"visa_required_for_italians":False,"currency":"MXN","language":"Spanish","climate_in_best_months":"Warm and sunny","flag_emoji":"🇲🇽","lat":21.16,"lon":-86.85},
        {"destination":"Medellín","country":"Colombia","continent":"Americas","tourist_spots":["Comuna 13","Plaza Botero","Guatapé","Parque Arví","El Poblado"],"avg_flight_cost_eur":850,"avg_hotel_7nights_full_board":650,"avg_hotel_7nights_half_board":520,"local_daily_expenses_eur":35,"best_months":["December","January","February","July","August"],"geopolitical_risk":"medium","conflict_zone":False,"active_warnings":["Some crime risk"],"value_score":8.9,"highlights":["Comuna 13","Plaza Botero","Guatapé"],"visa_required_for_italians":False,"currency":"COP","language":"Spanish","climate_in_best_months":"Dry and warm","flag_emoji":"🇨🇴","lat":6.25,"lon":-75.57},
        {"destination":"Rio de Janeiro","country":"Brazil","continent":"Americas","tourist_spots":["Christ the Redeemer","Sugarloaf","Copacabana","Ipanema","Tijuca Forest"],"avg_flight_cost_eur":950,"avg_hotel_7nights_full_board":1000,"avg_hotel_7nights_half_board":800,"local_daily_expenses_eur":55,"best_months":["December","January","February","March","July","August"],"geopolitical_risk":"medium","conflict_zone":False,"active_warnings":["Crime in some areas"],"value_score":8.1,"highlights":["Christ the Redeemer","Sugarloaf","Copacabana"],"visa_required_for_italians":False,"currency":"BRL","language":"Portuguese","climate_in_best_months":"Summer or mild winter","flag_emoji":"🇧🇷","lat":-22.91,"lon":-43.17},
        {"destination":"Buenos Aires","country":"Argentina","continent":"Americas","tourist_spots":["La Boca","Recoleta Cemetery","Teatro Colón","San Telmo Market","Palermo"],"avg_flight_cost_eur":1000,"avg_hotel_7nights_full_board":850,"avg_hotel_7nights_half_board":680,"local_daily_expenses_eur":45,"best_months":["September","October","November","March","April","May"],"geopolitical_risk":"low","conflict_zone":False,"active_warnings":["Economic protests"],"value_score":8.4,"highlights":["La Boca","Recoleta Cemetery","Teatro Colón"],"visa_required_for_italians":False,"currency":"ARS","language":"Spanish","climate_in_best_months":"Mild and pleasant","flag_emoji":"🇦🇷","lat":-34.60,"lon":-58.38},
        # OCEANIA
        {"destination":"Sydney","country":"Australia","continent":"Oceania","tourist_spots":["Opera House","Harbour Bridge","Bondi Beach","Blue Mountains","Taronga Zoo"],"avg_flight_cost_eur":1500,"avg_hotel_7nights_full_board":1400,"avg_hotel_7nights_half_board":1120,"local_daily_expenses_eur":80,"best_months":["September","October","November","March","April","May"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":7.8,"highlights":["Opera House","Harbour Bridge","Bondi Beach"],"visa_required_for_italians":True,"currency":"AUD","language":"English","climate_in_best_months":"Mild to warm","flag_emoji":"🇦🇺","lat":-33.87,"lon":151.21},
        {"destination":"Queenstown","country":"New Zealand","continent":"Oceania","tourist_spots":["Milford Sound","Bungee Jumping","Lake Wakatipu","Fiordland NP","Skydiving"],"avg_flight_cost_eur":1600,"avg_hotel_7nights_full_board":1300,"avg_hotel_7nights_half_board":1040,"local_daily_expenses_eur":70,"best_months":["December","January","February","June","July","August"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":8.5,"highlights":["Adventure sports","Milford Sound","Lake Wakatipu"],"visa_required_for_italians":True,"currency":"NZD","language":"English","climate_in_best_months":"Summer or snowy winter","flag_emoji":"🇳🇿","lat":-45.03,"lon":168.66},
        {"destination":"Nadi","country":"Fiji","continent":"Oceania","tourist_spots":["Coral Coast","Mamanuca Islands","Sabeto Hot Springs","Garden of the Sleeping Giant","Sigatoka Sand Dunes"],"avg_flight_cost_eur":1700,"avg_hotel_7nights_full_board":1200,"avg_hotel_7nights_half_board":960,"local_daily_expenses_eur":60,"best_months":["May","June","July","August","September","October"],"geopolitical_risk":"low","conflict_zone":False,"active_warnings":[],"value_score":8.3,"highlights":["Coral Coast","Island hopping","Sabeto Hot Springs"],"visa_required_for_italians":False,"currency":"FJD","language":"Fijian","climate_in_best_months":"Dry and sunny","flag_emoji":"🇫🇯","lat":-17.78,"lon":177.43},
        # MIDDLE EAST
        {"destination":"Dubai","country":"UAE","continent":"Middle East","tourist_spots":["Burj Khalifa","Dubai Mall","Desert Safari","Palm Jumeirah","Dubai Creek"],"avg_flight_cost_eur":500,"avg_hotel_7nights_full_board":1100,"avg_hotel_7nights_half_board":880,"local_daily_expenses_eur":80,"best_months":["November","December","January","February","March"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":8.2,"highlights":["Burj Khalifa","Dubai Mall","Desert Safari"],"visa_required_for_italians":False,"currency":"AED","language":"Arabic","climate_in_best_months":"Pleasant and mild","flag_emoji":"🇦🇪","lat":25.20,"lon":55.27},
        {"destination":"Muscat","country":"Oman","continent":"Middle East","tourist_spots":["Sultan Qaboos Mosque","Mutrah Souq","Wadi Shab","Nizwa Fort","Wahiba Sands"],"avg_flight_cost_eur":550,"avg_hotel_7nights_full_board":900,"avg_hotel_7nights_half_board":720,"local_daily_expenses_eur":60,"best_months":["October","November","December","January","February","March"],"geopolitical_risk":"minimal","conflict_zone":False,"active_warnings":[],"value_score":8.7,"highlights":["Sultan Qaboos Mosque","Mutrah Souq","Wadi Shab"],"visa_required_for_italians":False,"currency":"OMR","language":"Arabic","climate_in_best_months":"Cool and dry","flag_emoji":"🇴🇲","lat":23.58,"lon":58.40},
        {"destination":"Amman","country":"Jordan","continent":"Middle East","tourist_spots":["Petra","Dead Sea","Roman Amphitheatre","Jerash","Wadi Rum"],"avg_flight_cost_eur":400,"avg_hotel_7nights_full_board":750,"avg_hotel_7nights_half_board":600,"local_daily_expenses_eur":50,"best_months":["March","April","May","September","October","November"],"geopolitical_risk":"medium","conflict_zone":False,"active_warnings":[],"value_score":8.0,"highlights":["Petra","Dead Sea","Roman Amphitheatre"],"visa_required_for_italians":True,"currency":"JOD","language":"Arabic","climate_in_best_months":"Mild and sunny","flag_emoji":"🇯🇴","lat":31.95,"lon":35.93},
    ]
    for d in destinations:
        if d["geopolitical_risk"] == "critical" or d["conflict_zone"]:
            raise ValueError(f"Conflict zone found: {d['destination']}")
    return destinations

DESTINATION_DATABASE = load_destinations()

# ------------------------------------------------------------------------------
# HOTEL SEARCH via OpenStreetMap Nominatim + Overpass API (free, no key needed)
@st.cache_data(ttl=3600, show_spinner=False)
def search_hotels_overpass(city: str, lat: float, lon: float, min_stars: int) -> pd.DataFrame:
    """
    Query Overpass API (OpenStreetMap) for hotels near a city.
    Returns a DataFrame with name, stars, address, website.
    """
    radius = 5000  # 5km radius
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][timeout:25];
    (
      node["tourism"="hotel"]["stars"~"^[{min_stars}-5]"](around:{radius},{lat},{lon});
      way["tourism"="hotel"]["stars"~"^[{min_stars}-5]"](around:{radius},{lat},{lon});
    );
    out body;
    """
    try:
        resp = requests.post(overpass_url, data={"data": query}, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        hotels = []
        seen = set()
        for el in data.get("elements", []):
            tags = el.get("tags", {})
            name = tags.get("name", "")
            if not name or name in seen:
                continue
            seen.add(name)
            stars_raw = tags.get("stars", tags.get("star_rating", ""))
            try:
                stars = int(float(stars_raw))
            except (ValueError, TypeError):
                stars = 0
            if stars < min_stars:
                continue
            addr_parts = [
                tags.get("addr:street", ""),
                tags.get("addr:housenumber", ""),
                tags.get("addr:city", city)
            ]
            address = " ".join(p for p in addr_parts if p).strip() or city
            hotels.append({
                "name": name,
                "stars": stars,
                "stars_display": "⭐" * stars if stars > 0 else "N/A",
                "address": address,
                "website": tags.get("website", tags.get("contact:website", "")),
                "phone": tags.get("phone", tags.get("contact:phone", "")),
                "checkin": tags.get("check_in", ""),
                "checkout": tags.get("check_out", ""),
            })
        df = pd.DataFrame(hotels)
        if not df.empty:
            df = df[df["stars"] >= min_stars].sort_values("stars", ascending=False).reset_index(drop=True)
        return df
    except Exception as e:
        return pd.DataFrame()

# ------------------------------------------------------------------------------
# HELPERS
def format_eur(value: float) -> str:
    return f"€{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def get_month_options() -> List[str]:
    now = datetime.now()
    return [calendar.month_name[((now.month - 1 + i) % 12) + 1] for i in range(12)]

def calculate_total_cost(dest: Dict, config: Dict) -> float:
    flight = dest["avg_flight_cost_eur"] if config["with_flight"] else 0
    hotel_7 = dest["avg_hotel_7nights_full_board"] if config["board_type"] == "Full Board 🍽️" else dest["avg_hotel_7nights_half_board"]
    hotel = (hotel_7 / 7) * config["trip_duration"]
    local = dest["local_daily_expenses_eur"] * config["trip_duration"]
    return (flight + hotel + local) * config["travelers"]

def filter_and_rank(database: List[Dict], user_config: Dict, budget_total: float) -> pd.DataFrame:
    risk_map = {
        "Zero Risk (war-free, protest-free)": ["minimal"],
        "Low Risk (minor alerts only)": ["minimal", "low"],
        "Medium Risk (traveler's caution)": ["minimal", "low", "medium"]
    }
    allowed_risks = risk_map[user_config["risk_tolerance"]]
    selected_continents = user_config["continent_filter"]
    selected_countries   = user_config["country_filter"]
    selected_cities      = user_config["city_filter"]
    selected_months      = user_config["travel_month"]

    filtered = []
    for d in database:
        if d["geopolitical_risk"] not in allowed_risks:
            continue
        if "All" not in selected_continents and d["continent"] not in selected_continents:
            continue
        if selected_countries and "All" not in selected_countries and d["country"] not in selected_countries:
            continue
        if selected_cities and "All" not in selected_cities and d["destination"] not in selected_cities:
            continue
        if selected_months and not any(m in d["best_months"] for m in selected_months):
            continue
        total_cost = calculate_total_cost(d, user_config)
        if total_cost > budget_total:
            continue
        safety_bonus    = {"minimal": 10, "low": 8, "medium": 5}.get(d["geopolitical_risk"], 0)
        budget_fit      = max(0, 10 - (total_cost / budget_total) * 10)
        smart_score     = (d["value_score"] * 0.4) + (safety_bonus * 0.3) + (budget_fit * 0.3)
        filtered.append({**d, "total_cost_eur": total_cost, "smart_score": round(smart_score, 2),
                         "safety_bonus": safety_bonus, "budget_fit_score": round(budget_fit, 2)})
    df = pd.DataFrame(filtered)
    if not df.empty:
        df = df.sort_values("smart_score", ascending=False).reset_index(drop=True)
    return df

# ------------------------------------------------------------------------------
# BUILD CASCADING FILTER OPTIONS
all_continents = sorted(set(d["continent"]   for d in DESTINATION_DATABASE))
all_countries  = sorted(set(d["country"]     for d in DESTINATION_DATABASE))
all_cities     = sorted(set(d["destination"] for d in DESTINATION_DATABASE))

# ------------------------------------------------------------------------------
# SIDEBAR
st.sidebar.title("✈️ Travel Configuration")
st.sidebar.markdown("### 🌍 Where to go?")

continent_filter = st.sidebar.multiselect("Continent", ["All"] + all_continents, default=["All"])

# Dynamic country list based on selected continents
if "All" in continent_filter or not continent_filter:
    country_choices = all_countries
else:
    country_choices = sorted(set(d["country"] for d in DESTINATION_DATABASE if d["continent"] in continent_filter))
country_filter = st.sidebar.multiselect("Country", ["All"] + country_choices, default=["All"])

# Dynamic city list based on selected countries
if "All" in country_filter or not country_filter:
    if "All" in continent_filter or not continent_filter:
        city_choices = all_cities
    else:
        city_choices = sorted(set(d["destination"] for d in DESTINATION_DATABASE if d["continent"] in continent_filter))
else:
    city_choices = sorted(set(d["destination"] for d in DESTINATION_DATABASE if d["country"] in country_filter))
city_filter = st.sidebar.multiselect("City / Locality", ["All"] + city_choices, default=["All"])

st.sidebar.markdown("### ✈️ Trip Settings")
travel_mode      = st.sidebar.radio("Travel Mode",  ["With Flight ✈️", "Without Flight 🚗🚢"])
board_type       = st.sidebar.radio("Board Type",   ["Full Board 🍽️", "Half Board 🥗"])
budget_per_person= st.sidebar.slider("Budget per person (€)", 300, 5000, 1200, step=100)
travelers        = st.sidebar.number_input("Number of travelers", 1, 10, 2, step=1)
month_options    = get_month_options()
travel_month     = st.sidebar.multiselect("Travel month(s)", month_options, default=month_options[:3])
trip_duration    = st.sidebar.slider("Trip duration (days)", 3, 21, 7, step=1)
risk_tolerance   = st.sidebar.selectbox("Risk Tolerance",
    ["Zero Risk (war-free, protest-free)", "Low Risk (minor alerts only)", "Medium Risk (traveler's caution)"])

st.sidebar.markdown("### 🏨 Hotel Search")
hotel_stars      = st.sidebar.select_slider("Minimum hotel stars ⭐", options=[1,2,3,4,5], value=3)
search_hotels_cb = st.sidebar.checkbox("🔍 Search hotels via OpenStreetMap", value=True)

analyze_clicked  = st.sidebar.button("🔍 Analyze Destinations", type="primary")

# ------------------------------------------------------------------------------
# MAIN
st.title("TravelIQ — Smart Destination Analyzer ✈️")
today     = datetime.now().strftime("%d %B %Y")
next_year = (datetime.now().replace(day=1) + pd.DateOffset(months=12)).strftime("%B %Y")
st.info(f"📅 Analysis period: **{today}** → **{next_year}** (next 12 months)")

if not analyze_clicked:
    st.markdown("### 👈 Set your filters in the sidebar and click **Analyze Destinations**")

    # Show destination map preview
    preview_df = pd.DataFrame([{"City": d["destination"], "Country": d["country"],
                                  "Continent": d["continent"], "lat": d["lat"], "lon": d["lon"],
                                  "Value Score": d["value_score"]} for d in DESTINATION_DATABASE])
    st.markdown("#### 🗺️ All available destinations")
    fig_map = px.scatter_geo(preview_df, lat="lat", lon="lon", hover_name="City",
                              hover_data={"Country": True, "Value Score": True, "lat": False, "lon": False},
                              color="Continent", size="Value Score",
                              projection="natural earth", title="")
    fig_map.update_layout(height=450, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig_map, use_container_width=True)
    st.stop()

# --- Perform analysis ---
with st.spinner("Analyzing destinations..."):
    user_config = {
        "with_flight":      travel_mode == "With Flight ✈️",
        "board_type":       board_type,
        "trip_duration":    trip_duration,
        "travelers":        travelers,
        "risk_tolerance":   risk_tolerance,
        "continent_filter": continent_filter,
        "country_filter":   country_filter,
        "city_filter":      city_filter,
        "travel_month":     travel_month,
    }
    budget_total = budget_per_person * travelers
    results_df   = filter_and_rank(DESTINATION_DATABASE, user_config, budget_total)

col1, col2, col3 = st.columns(3)
col1.metric("🌍 Destinations Analyzed", len(DESTINATION_DATABASE))
col2.metric("✅ Matching Criteria",      len(results_df))
col3.metric("💶 Total Budget",           format_eur(budget_total))

if results_df.empty:
    st.warning("No destinations match your criteria. Try relaxing filters (budget, risk, months, continent).")
    st.stop()

# ------------------------------------------------------------------------------
# TOP DESTINATION CARDS
st.subheader(f"🏆 Top {min(9, len(results_df))} Destinations by Smart Score")
top_results = results_df.head(9)

for i in range(0, len(top_results), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        idx = i + j
        if idx >= len(top_results):
            break
        dest = top_results.iloc[idx]
        with col:
            st.markdown(f'<div class="card"><h2>{dest["flag_emoji"]} {dest["destination"]}, {dest["country"]}</h2></div>',
                        unsafe_allow_html=True)
            st.write(f"**Smart Score:** {dest['smart_score']}/10")
            st.progress(float(dest['smart_score']) / 10)
            st.markdown(f"**Total cost:** {format_eur(dest['total_cost_eur'])}")

            flight_cost       = dest['avg_flight_cost_eur'] if user_config["with_flight"] else 0
            hotel_7           = dest['avg_hotel_7nights_full_board'] if board_type == "Full Board 🍽️" else dest['avg_hotel_7nights_half_board']
            hotel_cost_scaled = (hotel_7 / 7) * trip_duration
            local_cost        = dest['local_daily_expenses_eur'] * trip_duration
            total_per_person  = flight_cost + hotel_cost_scaled + local_cost

            st.caption(f"✈️ Flight: {format_eur(flight_cost * travelers)}" if user_config["with_flight"] else "✈️ Flight: not included")
            st.caption(f"🏨 Hotel: {format_eur(hotel_cost_scaled * travelers)}")
            st.caption(f"☕ Local: {format_eur(local_cost * travelers)}")

            months_badges = " ".join([f'<span class="badge-blue">{m[:3]}</span>' for m in dest['best_months'][:4]])
            st.markdown(f"**Best months:** {months_badges}", unsafe_allow_html=True)

            risk = dest['geopolitical_risk']
            risk_badge = {'minimal': '<span class="badge-green">✅ Minimal</span>',
                          'low':     '<span class="badge-yellow">🟡 Low</span>',
                          'medium':  '<span class="badge-orange">🟠 Medium</span>'}.get(risk, "")
            st.markdown(f"**Risk:** {risk_badge}", unsafe_allow_html=True)

            if dest['active_warnings']:
                st.warning(f"⚠️ {', '.join(dest['active_warnings'])}")

            # Tourist spots
            with st.expander("📍 Top Tourist Spots"):
                for spot in dest.get("tourist_spots", dest["highlights"]):
                    st.markdown(f"- {spot}")

            st.caption(f"🪪 Visa: {'Yes' if dest['visa_required_for_italians'] else 'No'} | 💱 {dest['currency']} | 🗣️ {dest['language']}")

            # Cost deep dive
            with st.expander("📊 Cost Deep Dive"):
                cost_df = pd.DataFrame({
                    "Item": ["Flight (pp)", "Hotel (pp)", "Local (pp)", "Total pp", "Group total"],
                    "Cost": [flight_cost, hotel_cost_scaled, local_cost, total_per_person, total_per_person * travelers]
                })
                cost_df["Cost (€)"] = cost_df["Cost"].apply(format_eur)
                st.table(cost_df[["Item", "Cost (€)"]])
                st.markdown(f"**Climate:** {dest['climate_in_best_months']}")

            # Hotel search
            if search_hotels_cb:
                with st.expander(f"🏨 Hotels {hotel_stars}★+ in {dest['destination']}"):
                    with st.spinner("Querying OpenStreetMap..."):
                        hotels_df = search_hotels_overpass(
                            dest["destination"], dest["lat"], dest["lon"], hotel_stars)
                    if hotels_df.empty:
                        st.info(f"No {hotel_stars}★+ hotels found in OSM for {dest['destination']}. "
                                f"Try lowering the star filter or search on [Booking.com](https://www.booking.com/searchresults.html?ss={dest['destination'].replace(' ', '+')}).")
                    else:
                        st.caption(f"Found **{len(hotels_df)}** hotels via OpenStreetMap")
                        for _, h in hotels_df.head(8).iterrows():
                            web_link = f'<a href="{h["website"]}" target="_blank">🌐 Website</a>' if h["website"] else ""
                            st.markdown(f"""
                            <div class="hotel-card">
                                <h4>{h['stars_display']} {h['name']}</h4>
                                <p>📍 {h['address']}</p>
                                {'<p>📞 ' + h['phone'] + '</p>' if h['phone'] else ''}
                                {'<p>' + web_link + '</p>' if web_link else ''}
                            </div>
                            """, unsafe_allow_html=True)
                        booking_url = f"https://www.booking.com/searchresults.html?ss={dest['destination'].replace(' ', '+')}&stars={hotel_stars}"
                        st.markdown(f"[🔎 See more on Booking.com]({booking_url})")

# ------------------------------------------------------------------------------
# COMPARISON TABLE
st.subheader("📋 Full Comparison Table")
compare_cols = ["flag_emoji","destination","country","continent","smart_score","total_cost_eur","geopolitical_risk","best_months","value_score"]
table_df = results_df[compare_cols].copy()
table_df["total_cost_eur"] = table_df["total_cost_eur"].apply(format_eur)
table_df["best_months"]    = table_df["best_months"].apply(lambda x: ", ".join(x[:4]))
table_df.rename(columns={"flag_emoji":"","destination":"City","country":"Country","continent":"Continent",
    "smart_score":"Smart Score","total_cost_eur":"Total Cost","geopolitical_risk":"Risk",
    "best_months":"Best Months","value_score":"Value Score"}, inplace=True)
st.dataframe(table_df, use_container_width=True)

# ------------------------------------------------------------------------------
# ANALYTICS TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Cost Analysis", "🗺️ Map View", "📅 Travel Calendar",
    "⭐ Hotel Stats", "⚠️ Geopolitical Monitor"])

with tab1:
    top10 = results_df.nlargest(10, "total_cost_eur")[["destination","country","total_cost_eur"]].copy()
    top10["label"] = top10["destination"] + ", " + top10["country"]
    fig_bar = px.bar(top10, x="label", y="total_cost_eur",
                     title="Top 10 Destinations by Total Cost",
                     labels={"total_cost_eur":"Total Cost (€)","label":""}, color="total_cost_eur",
                     color_continuous_scale="Blues")
    st.plotly_chart(fig_bar, use_container_width=True)

    fig_sc = px.scatter(results_df, x="value_score", y="total_cost_eur", size="safety_bonus",
                        color="geopolitical_risk", hover_name="destination",
                        hover_data={"country": True},
                        title="Value Score vs Total Cost",
                        labels={"value_score":"Value Score (1-10)","total_cost_eur":"Total Cost (€)"})
    st.plotly_chart(fig_sc, use_container_width=True)

with tab2:
    map_df = results_df.copy()
    map_df["label"] = map_df["destination"] + ", " + map_df["country"]
    fig_map = px.scatter_geo(map_df, lat="lat", lon="lon", hover_name="label",
                              color="smart_score", size="value_score",
                              hover_data={"total_cost_eur": True, "geopolitical_risk": True, "lat": False, "lon": False},
                              color_continuous_scale="Viridis",
                              projection="natural earth", title="Filtered Destinations — Smart Score")
    fig_map.update_layout(height=500, margin=dict(l=0,r=0,t=30,b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    # Continent pie
    cont_df = results_df["continent"].value_counts().reset_index()
    cont_df.columns = ["continent","count"]
    fig_pie = px.pie(cont_df, names="continent", values="count", title="By Continent")
    st.plotly_chart(fig_pie, use_container_width=True)

    # Country breakdown
    country_df = results_df["country"].value_counts().reset_index()
    country_df.columns = ["Country","Destinations"]
    st.table(country_df)

with tab3:
    all_months_list = ["January","February","March","April","May","June",
                       "July","August","September","October","November","December"]
    heatmap_data = []
    dest_labels = (results_df["destination"] + ", " + results_df["country"]).tolist()
    for _, row in results_df.iterrows():
        heatmap_data.append([1 if m in row["best_months"] else 0 for m in all_months_list])
    fig_heat = go.Figure(data=go.Heatmap(
        z=heatmap_data, x=all_months_list, y=dest_labels,
        colorscale=[[0,"#1a1f35"],[1,"#4a90d9"]], showscale=False))
    fig_heat.update_layout(title="Best Months Heatmap", height=max(400, len(dest_labels)*22))
    st.plotly_chart(fig_heat, use_container_width=True)
    st.caption("🔵 Blue = best travel month. Selected: " + ", ".join(travel_month))

with tab4:
    st.markdown("### Hotel Star Distribution")
    st.info("The chart below shows estimated hotel category distribution for filtered destinations, "
            "based on average market data. Live OSM data is loaded per-destination inside each card above.")
    star_data = []
    for _, row in results_df.iterrows():
        base = row["avg_hotel_7nights_full_board"]
        star_data.append({"Destination": f"{row['destination']}, {row['country']}",
                          "3★ est. (€/7n)": round(base * 0.65),
                          "4★ est. (€/7n)": round(base * 1.0),
                          "5★ est. (€/7n)": round(base * 1.55)})
    star_df = pd.DataFrame(star_data)
    st.dataframe(star_df, use_container_width=True)

    fig_stars = px.bar(star_df.melt(id_vars="Destination", var_name="Category", value_name="€/7n"),
                       x="Destination", y="€/7n", color="Category", barmode="group",
                       title="Estimated Hotel Cost by Star Category (7 nights)",
                       color_discrete_map={"3★ est. (€/7n)":"#4a90d9",
                                           "4★ est. (€/7n)":"#f5a623",
                                           "5★ est. (€/7n)":"#e85d75"})
    fig_stars.update_layout(xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig_stars, use_container_width=True)

with tab5:
    st.subheader("Risk Overview")
    risk_df = results_df[["destination","country","geopolitical_risk","active_warnings"]].copy()
    risk_df["geopolitical_risk"] = risk_df["geopolitical_risk"].str.capitalize()
    risk_df["active_warnings"]   = risk_df["active_warnings"].apply(lambda x: "; ".join(x) if x else "None")
    st.dataframe(risk_df.rename(columns={"destination":"City","country":"Country",
        "geopolitical_risk":"Risk Level","active_warnings":"Warnings"}), use_container_width=True)

    st.subheader("🚫 Always-excluded conflict zones")
    excluded = ["Russia","Ukraine","Belarus","Sudan","Syria","Yemen","Myanmar",
                "Haiti","Gaza/West Bank","Libya","Mali","Burkina Faso","Niger",
                "North Korea","Afghanistan","Iraq","Somalia"]
    st.markdown(", ".join(f"**{e}**" for e in excluded))
    st.caption(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ------------------------------------------------------------------------------
# FOOTER
st.markdown("---")
st.markdown("""
**Disclaimer:** Data based on average market estimates. Hotel data sourced from OpenStreetMap contributors via Overpass API.  
Always verify advisories at [viaggiaresicuri.farnesina.it](https://viaggiaresicuri.farnesina.it).  
Powered by **TravelIQ Engine v2.0**
""")
