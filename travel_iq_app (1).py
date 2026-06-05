# travel_iq_app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar
from typing import Dict, List, Tuple, Any

# ------------------------------------------------------------------------------
# PAGE CONFIGURATION
st.set_page_config(
    layout="wide",
    page_title="TravelIQ — Smart Destination Analyzer",
    page_icon="✈️"
)

# Custom CSS for cards and badges — dark-theme compatible
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
    .card:hover {
        transform: translateY(-4px);
        background-color: #363c6a;
    }
    .card h2 {
        color: #e8eeff !important;
        font-size: 1.1rem;
        margin: 0;
        line-height: 1.4;
    }
    .badge-green {
        background-color: #1a7a3c;
        color: #b6ffce;
        padding: 0.2rem 0.65rem;
        border-radius: 30px;
        font-size: 0.78rem;
        display: inline-block;
        font-weight: 600;
    }
    .badge-yellow {
        background-color: #7a6200;
        color: #ffe899;
        padding: 0.2rem 0.65rem;
        border-radius: 30px;
        font-size: 0.78rem;
        display: inline-block;
        font-weight: 600;
    }
    .badge-orange {
        background-color: #7a3400;
        color: #ffbd85;
        padding: 0.2rem 0.65rem;
        border-radius: 30px;
        font-size: 0.78rem;
        display: inline-block;
        font-weight: 600;
    }
    .badge-blue {
        background-color: #0a3d7a;
        color: #a8d4ff;
        padding: 0.2rem 0.65rem;
        border-radius: 30px;
        font-size: 0.78rem;
        display: inline-block;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# DESTINATION DATABASE (40+ destinations, no conflict zones / critical risk)
def load_destinations() -> List[Dict]:
    destinations = []

    # EUROPE
    destinations.extend([
        {"destination": "Lisbon, Portugal", "continent": "Europe", "avg_flight_cost_eur": 150, "avg_hotel_7nights_full_board": 700, "avg_hotel_7nights_half_board": 560, "local_daily_expenses_eur": 45, "best_months": ["March", "April", "May", "September", "October"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 8.7, "highlights": ["Belém Tower", "Tram 28 Ride", "Pastéis de Belém"], "visa_required_for_italians": False, "currency": "EUR", "language": "Portuguese", "climate_in_best_months": "Mild and sunny", "flag_emoji": "🇵🇹"},
        {"destination": "Porto, Portugal", "continent": "Europe", "avg_flight_cost_eur": 140, "avg_hotel_7nights_full_board": 650, "avg_hotel_7nights_half_board": 520, "local_daily_expenses_eur": 40, "best_months": ["May", "June", "September"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 8.9, "highlights": ["Dom Luís I Bridge", "Port Wine Cellars", "Ribeira District"], "visa_required_for_italians": False, "currency": "EUR", "language": "Portuguese", "climate_in_best_months": "Warm and dry", "flag_emoji": "🇵🇹"},
        {"destination": "Barcelona, Spain", "continent": "Europe", "avg_flight_cost_eur": 120, "avg_hotel_7nights_full_board": 800, "avg_hotel_7nights_half_board": 640, "local_daily_expenses_eur": 60, "best_months": ["April", "May", "June", "September", "October"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": ["Petty crime risk in crowded areas"], "value_score": 8.2, "highlights": ["Sagrada Familia", "Park Güell", "Las Ramblas"], "visa_required_for_italians": False, "currency": "EUR", "language": "Spanish", "climate_in_best_months": "Warm and pleasant", "flag_emoji": "🇪🇸"},
        {"destination": "Madrid, Spain", "continent": "Europe", "avg_flight_cost_eur": 130, "avg_hotel_7nights_full_board": 780, "avg_hotel_7nights_half_board": 620, "local_daily_expenses_eur": 55, "best_months": ["April", "May", "June", "September", "October"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 8.1, "highlights": ["Prado Museum", "Royal Palace", "Retiro Park"], "visa_required_for_italians": False, "currency": "EUR", "language": "Spanish", "climate_in_best_months": "Mild and sunny", "flag_emoji": "🇪🇸"},
        {"destination": "Rome, Italy", "continent": "Europe", "avg_flight_cost_eur": 80, "avg_hotel_7nights_full_board": 900, "avg_hotel_7nights_half_board": 720, "local_daily_expenses_eur": 65, "best_months": ["April", "May", "June", "September", "October"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 7.9, "highlights": ["Colosseum", "Vatican City", "Trevi Fountain"], "visa_required_for_italians": False, "currency": "EUR", "language": "Italian", "climate_in_best_months": "Warm and sunny", "flag_emoji": "🇮🇹"},
        {"destination": "Florence, Italy", "continent": "Europe", "avg_flight_cost_eur": 100, "avg_hotel_7nights_full_board": 850, "avg_hotel_7nights_half_board": 680, "local_daily_expenses_eur": 60, "best_months": ["April", "May", "June", "September", "October"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 8.3, "highlights": ["Uffizi Gallery", "Duomo", "Ponte Vecchio"], "visa_required_for_italians": False, "currency": "EUR", "language": "Italian", "climate_in_best_months": "Mild and pleasant", "flag_emoji": "🇮🇹"},
        {"destination": "Paris, France", "continent": "Europe", "avg_flight_cost_eur": 110, "avg_hotel_7nights_full_board": 1100, "avg_hotel_7nights_half_board": 880, "local_daily_expenses_eur": 80, "best_months": ["April", "May", "June", "September", "October"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": ["Strike disruptions possible"], "value_score": 7.5, "highlights": ["Eiffel Tower", "Louvre", "Notre-Dame"], "visa_required_for_italians": False, "currency": "EUR", "language": "French", "climate_in_best_months": "Mild and pleasant", "flag_emoji": "🇫🇷"},
        {"destination": "Athens, Greece", "continent": "Europe", "avg_flight_cost_eur": 180, "avg_hotel_7nights_full_board": 750, "avg_hotel_7nights_half_board": 600, "local_daily_expenses_eur": 55, "best_months": ["April", "May", "June", "September", "October"], "geopolitical_risk": "low", "conflict_zone": False, "active_warnings": [], "value_score": 8.0, "highlights": ["Acropolis", "Plaka", "Temple of Olympian Zeus"], "visa_required_for_italians": False, "currency": "EUR", "language": "Greek", "climate_in_best_months": "Warm and dry", "flag_emoji": "🇬🇷"},
        {"destination": "Budapest, Hungary", "continent": "Europe", "avg_flight_cost_eur": 160, "avg_hotel_7nights_full_board": 600, "avg_hotel_7nights_half_board": 480, "local_daily_expenses_eur": 45, "best_months": ["April", "May", "June", "September", "October"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 9.0, "highlights": ["Buda Castle", "Parliament", "Széchenyi Baths"], "visa_required_for_italians": False, "currency": "HUF", "language": "Hungarian", "climate_in_best_months": "Mild and sunny", "flag_emoji": "🇭🇺"},
        {"destination": "Krakow, Poland", "continent": "Europe", "avg_flight_cost_eur": 130, "avg_hotel_7nights_full_board": 550, "avg_hotel_7nights_half_board": 440, "local_daily_expenses_eur": 40, "best_months": ["May", "June", "July", "August", "September"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 9.2, "highlights": ["Wawel Castle", "Main Market Square", "Auschwitz-Birkenau"], "visa_required_for_italians": False, "currency": "PLN", "language": "Polish", "climate_in_best_months": "Warm and pleasant", "flag_emoji": "🇵🇱"},
    ])

    # ASIA
    destinations.extend([
        {"destination": "Tokyo, Japan", "continent": "Asia", "avg_flight_cost_eur": 1000, "avg_hotel_7nights_full_board": 1400, "avg_hotel_7nights_half_board": 1120, "local_daily_expenses_eur": 70, "best_months": ["March", "April", "October", "November"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 8.4, "highlights": ["Shibuya Crossing", "Senso-ji Temple", "Tokyo Tower"], "visa_required_for_italians": False, "currency": "JPY", "language": "Japanese", "climate_in_best_months": "Cherry blossoms or mild autumn", "flag_emoji": "🇯🇵"},
        {"destination": "Kyoto, Japan", "continent": "Asia", "avg_flight_cost_eur": 1050, "avg_hotel_7nights_full_board": 1350, "avg_hotel_7nights_half_board": 1080, "local_daily_expenses_eur": 65, "best_months": ["March", "April", "October", "November"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 8.6, "highlights": ["Fushimi Inari", "Kinkaku-ji", "Arashiyama Bamboo"], "visa_required_for_italians": False, "currency": "JPY", "language": "Japanese", "climate_in_best_months": "Cherry blossoms or colorful leaves", "flag_emoji": "🇯🇵"},
        {"destination": "Bangkok, Thailand", "continent": "Asia", "avg_flight_cost_eur": 750, "avg_hotel_7nights_full_board": 600, "avg_hotel_7nights_half_board": 480, "local_daily_expenses_eur": 35, "best_months": ["November", "December", "January", "February"], "geopolitical_risk": "low", "conflict_zone": False, "active_warnings": ["Occasional political protests"], "value_score": 9.0, "highlights": ["Grand Palace", "Wat Arun", "Chatuchak Market"], "visa_required_for_italians": False, "currency": "THB", "language": "Thai", "climate_in_best_months": "Cool and dry", "flag_emoji": "🇹🇭"},
        {"destination": "Chiang Mai, Thailand", "continent": "Asia", "avg_flight_cost_eur": 800, "avg_hotel_7nights_full_board": 500, "avg_hotel_7nights_half_board": 400, "local_daily_expenses_eur": 30, "best_months": ["November", "December", "January", "February"], "geopolitical_risk": "low", "conflict_zone": False, "active_warnings": [], "value_score": 9.3, "highlights": ["Doi Suthep", "Old City Temples", "Night Bazaar"], "visa_required_for_italians": False, "currency": "THB", "language": "Thai", "climate_in_best_months": "Cool and pleasant", "flag_emoji": "🇹🇭"},
        {"destination": "Bali, Indonesia", "continent": "Asia", "avg_flight_cost_eur": 900, "avg_hotel_7nights_full_board": 800, "avg_hotel_7nights_half_board": 640, "local_daily_expenses_eur": 40, "best_months": ["April", "May", "June", "July", "August", "September"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 8.8, "highlights": ["Ubud Rice Terraces", "Tanah Lot", "Mount Batur"], "visa_required_for_italians": False, "currency": "IDR", "language": "Indonesian", "climate_in_best_months": "Dry season", "flag_emoji": "🇮🇩"},
        {"destination": "Seoul, South Korea", "continent": "Asia", "avg_flight_cost_eur": 850, "avg_hotel_7nights_full_board": 1100, "avg_hotel_7nights_half_board": 880, "local_daily_expenses_eur": 60, "best_months": ["April", "May", "September", "October"], "geopolitical_risk": "low", "conflict_zone": False, "active_warnings": [], "value_score": 8.3, "highlights": ["Gyeongbokgung Palace", "N Seoul Tower", "Myeongdong"], "visa_required_for_italians": False, "currency": "KRW", "language": "Korean", "climate_in_best_months": "Mild and sunny", "flag_emoji": "🇰🇷"},
        {"destination": "Hanoi, Vietnam", "continent": "Asia", "avg_flight_cost_eur": 800, "avg_hotel_7nights_full_board": 550, "avg_hotel_7nights_half_board": 440, "local_daily_expenses_eur": 30, "best_months": ["October", "November", "December", "January", "February", "March"], "geopolitical_risk": "low", "conflict_zone": False, "active_warnings": [], "value_score": 9.1, "highlights": ["Hoan Kiem Lake", "Old Quarter", "Ha Long Bay day trip"], "visa_required_for_italians": False, "currency": "VND", "language": "Vietnamese", "climate_in_best_months": "Cool and dry", "flag_emoji": "🇻🇳"},
        {"destination": "Siem Reap, Cambodia", "continent": "Asia", "avg_flight_cost_eur": 850, "avg_hotel_7nights_full_board": 500, "avg_hotel_7nights_half_board": 400, "local_daily_expenses_eur": 30, "best_months": ["November", "December", "January", "February", "March"], "geopolitical_risk": "low", "conflict_zone": False, "active_warnings": [], "value_score": 9.4, "highlights": ["Angkor Wat", "Tonle Sap", "Pub Street"], "visa_required_for_italians": True, "currency": "KHR", "language": "Khmer", "climate_in_best_months": "Cool and dry", "flag_emoji": "🇰🇭"},
        {"destination": "Hoi An, Vietnam", "continent": "Asia", "avg_flight_cost_eur": 820, "avg_hotel_7nights_full_board": 480, "avg_hotel_7nights_half_board": 380, "local_daily_expenses_eur": 28, "best_months": ["February", "March", "April", "May", "June", "July", "August"], "geopolitical_risk": "low", "conflict_zone": False, "active_warnings": [], "value_score": 9.5, "highlights": ["Ancient Town", "Japanese Bridge", "Tailor Shops"], "visa_required_for_italians": False, "currency": "VND", "language": "Vietnamese", "climate_in_best_months": "Warm and dry", "flag_emoji": "🇻🇳"},
    ])

    # AFRICA
    destinations.extend([
        {"destination": "Marrakech, Morocco", "continent": "Africa", "avg_flight_cost_eur": 250, "avg_hotel_7nights_full_board": 650, "avg_hotel_7nights_half_board": 520, "local_daily_expenses_eur": 40, "best_months": ["March", "April", "May", "September", "October", "November"], "geopolitical_risk": "low", "conflict_zone": False, "active_warnings": [], "value_score": 8.5, "highlights": ["Jemaa el-Fnaa", "Bahia Palace", "Majorelle Garden"], "visa_required_for_italians": False, "currency": "MAD", "language": "Arabic", "climate_in_best_months": "Warm and sunny", "flag_emoji": "🇲🇦"},
        {"destination": "Cape Town, South Africa", "continent": "Africa", "avg_flight_cost_eur": 850, "avg_hotel_7nights_full_board": 950, "avg_hotel_7nights_half_board": 760, "local_daily_expenses_eur": 55, "best_months": ["November", "December", "January", "February", "March"], "geopolitical_risk": "medium", "conflict_zone": False, "active_warnings": ["Crime in certain areas"], "value_score": 8.0, "highlights": ["Table Mountain", "Robben Island", "Cape Winelands"], "visa_required_for_italians": False, "currency": "ZAR", "language": "Afrikaans", "climate_in_best_months": "Dry and warm", "flag_emoji": "🇿🇦"},
        {"destination": "Zanzibar, Tanzania", "continent": "Africa", "avg_flight_cost_eur": 750, "avg_hotel_7nights_full_board": 1100, "avg_hotel_7nights_half_board": 880, "local_daily_expenses_eur": 50, "best_months": ["June", "July", "August", "September", "October", "December", "January", "February"], "geopolitical_risk": "low", "conflict_zone": False, "active_warnings": [], "value_score": 8.2, "highlights": ["Stone Town", "Nakupenda Beach", "Spice Tour"], "visa_required_for_italians": True, "currency": "TZS", "language": "Swahili", "climate_in_best_months": "Dry and sunny", "flag_emoji": "🇹🇿"},
        {"destination": "Djerba, Tunisia", "continent": "Africa", "avg_flight_cost_eur": 220, "avg_hotel_7nights_full_board": 600, "avg_hotel_7nights_half_board": 480, "local_daily_expenses_eur": 35, "best_months": ["April", "May", "June", "September", "October"], "geopolitical_risk": "medium", "conflict_zone": False, "active_warnings": ["Occasional security alerts"], "value_score": 8.7, "highlights": ["Houmt Souk", "El Ghriba Synagogue", "Flamingo Beach"], "visa_required_for_italians": False, "currency": "TND", "language": "Arabic", "climate_in_best_months": "Warm and sunny", "flag_emoji": "🇹🇳"},
    ])

    # AMERICAS
    destinations.extend([
        {"destination": "Mexico City, Mexico", "continent": "Americas", "avg_flight_cost_eur": 800, "avg_hotel_7nights_full_board": 700, "avg_hotel_7nights_half_board": 560, "local_daily_expenses_eur": 45, "best_months": ["March", "April", "May", "October", "November"], "geopolitical_risk": "medium", "conflict_zone": False, "active_warnings": ["Petty crime, occasional protests"], "value_score": 8.2, "highlights": ["Teotihuacan", "Frida Kahlo Museum", "Zócalo"], "visa_required_for_italians": False, "currency": "MXN", "language": "Spanish", "climate_in_best_months": "Mild and dry", "flag_emoji": "🇲🇽"},
        {"destination": "Cancún, Mexico", "continent": "Americas", "avg_flight_cost_eur": 850, "avg_hotel_7nights_full_board": 1200, "avg_hotel_7nights_half_board": 960, "local_daily_expenses_eur": 60, "best_months": ["December", "January", "February", "March", "April"], "geopolitical_risk": "low", "conflict_zone": False, "active_warnings": [], "value_score": 8.0, "highlights": ["Mayan Ruins", "Beaches", "Isla Mujeres"], "visa_required_for_italians": False, "currency": "MXN", "language": "Spanish", "climate_in_best_months": "Warm and sunny", "flag_emoji": "🇲🇽"},
        {"destination": "Medellín, Colombia", "continent": "Americas", "avg_flight_cost_eur": 850, "avg_hotel_7nights_full_board": 650, "avg_hotel_7nights_half_board": 520, "local_daily_expenses_eur": 35, "best_months": ["December", "January", "February", "July", "August"], "geopolitical_risk": "medium", "conflict_zone": False, "active_warnings": ["Some crime risk"], "value_score": 8.9, "highlights": ["Comuna 13", "Plaza Botero", "Guatapé"], "visa_required_for_italians": False, "currency": "COP", "language": "Spanish", "climate_in_best_months": "Dry and warm", "flag_emoji": "🇨🇴"},
        {"destination": "Rio de Janeiro, Brazil", "continent": "Americas", "avg_flight_cost_eur": 950, "avg_hotel_7nights_full_board": 1000, "avg_hotel_7nights_half_board": 800, "local_daily_expenses_eur": 55, "best_months": ["December", "January", "February", "March", "July", "August"], "geopolitical_risk": "medium", "conflict_zone": False, "active_warnings": ["Crime in some areas"], "value_score": 8.1, "highlights": ["Christ the Redeemer", "Sugarloaf", "Copacabana"], "visa_required_for_italians": False, "currency": "BRL", "language": "Portuguese", "climate_in_best_months": "Summer or mild winter", "flag_emoji": "🇧🇷"},
        {"destination": "Buenos Aires, Argentina", "continent": "Americas", "avg_flight_cost_eur": 1000, "avg_hotel_7nights_full_board": 850, "avg_hotel_7nights_half_board": 680, "local_daily_expenses_eur": 45, "best_months": ["September", "October", "November", "March", "April", "May"], "geopolitical_risk": "low", "conflict_zone": False, "active_warnings": ["Economic protests"], "value_score": 8.4, "highlights": ["La Boca", "Recoleta Cemetery", "Teatro Colón"], "visa_required_for_italians": False, "currency": "ARS", "language": "Spanish", "climate_in_best_months": "Mild and pleasant", "flag_emoji": "🇦🇷"},
    ])

    # OCEANIA
    destinations.extend([
        {"destination": "Sydney, Australia", "continent": "Oceania", "avg_flight_cost_eur": 1500, "avg_hotel_7nights_full_board": 1400, "avg_hotel_7nights_half_board": 1120, "local_daily_expenses_eur": 80, "best_months": ["September", "October", "November", "March", "April", "May"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 7.8, "highlights": ["Opera House", "Harbour Bridge", "Bondi Beach"], "visa_required_for_italians": True, "currency": "AUD", "language": "English", "climate_in_best_months": "Mild to warm", "flag_emoji": "🇦🇺"},
        {"destination": "Queenstown, New Zealand", "continent": "Oceania", "avg_flight_cost_eur": 1600, "avg_hotel_7nights_full_board": 1300, "avg_hotel_7nights_half_board": 1040, "local_daily_expenses_eur": 70, "best_months": ["December", "January", "February", "June", "July", "August"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 8.5, "highlights": ["Adventure sports", "Milford Sound", "Lake Wakatipu"], "visa_required_for_italians": True, "currency": "NZD", "language": "English", "climate_in_best_months": "Summer or snowy winter", "flag_emoji": "🇳🇿"},
        {"destination": "Nadi, Fiji", "continent": "Oceania", "avg_flight_cost_eur": 1700, "avg_hotel_7nights_full_board": 1200, "avg_hotel_7nights_half_board": 960, "local_daily_expenses_eur": 60, "best_months": ["May", "June", "July", "August", "September", "October"], "geopolitical_risk": "low", "conflict_zone": False, "active_warnings": [], "value_score": 8.3, "highlights": ["Coral Coast", "Island hopping", "Sabeto Hot Springs"], "visa_required_for_italians": False, "currency": "FJD", "language": "Fijian", "climate_in_best_months": "Dry and sunny", "flag_emoji": "🇫🇯"},
    ])

    # MIDDLE EAST
    destinations.extend([
        {"destination": "Dubai, UAE", "continent": "Middle East", "avg_flight_cost_eur": 500, "avg_hotel_7nights_full_board": 1100, "avg_hotel_7nights_half_board": 880, "local_daily_expenses_eur": 80, "best_months": ["November", "December", "January", "February", "March"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 8.2, "highlights": ["Burj Khalifa", "Dubai Mall", "Desert Safari"], "visa_required_for_italians": False, "currency": "AED", "language": "Arabic", "climate_in_best_months": "Pleasant and mild", "flag_emoji": "🇦🇪"},
        {"destination": "Muscat, Oman", "continent": "Middle East", "avg_flight_cost_eur": 550, "avg_hotel_7nights_full_board": 900, "avg_hotel_7nights_half_board": 720, "local_daily_expenses_eur": 60, "best_months": ["October", "November", "December", "January", "February", "March"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 8.7, "highlights": ["Sultan Qaboos Mosque", "Mutrah Souq", "Wadi Shab"], "visa_required_for_italians": False, "currency": "OMR", "language": "Arabic", "climate_in_best_months": "Cool and dry", "flag_emoji": "🇴🇲"},
        {"destination": "Amman, Jordan", "continent": "Middle East", "avg_flight_cost_eur": 400, "avg_hotel_7nights_full_board": 750, "avg_hotel_7nights_half_board": 600, "local_daily_expenses_eur": 50, "best_months": ["March", "April", "May", "September", "October", "November"], "geopolitical_risk": "medium", "conflict_zone": False, "active_warnings": [], "value_score": 8.0, "highlights": ["Petra", "Dead Sea", "Roman Amphitheatre"], "visa_required_for_italians": True, "currency": "JOD", "language": "Arabic", "climate_in_best_months": "Mild and sunny", "flag_emoji": "🇯🇴"},
    ])

    destinations.extend([
        {"destination": "Reykjavik, Iceland", "continent": "Europe", "avg_flight_cost_eur": 250, "avg_hotel_7nights_full_board": 1300, "avg_hotel_7nights_half_board": 1040, "local_daily_expenses_eur": 100, "best_months": ["June", "July", "August", "September"], "geopolitical_risk": "minimal", "conflict_zone": False, "active_warnings": [], "value_score": 7.5, "highlights": ["Northern Lights", "Blue Lagoon", "Golden Circle"], "visa_required_for_italians": False, "currency": "ISK", "language": "Icelandic", "climate_in_best_months": "Mild and bright nights", "flag_emoji": "🇮🇸"},
    ])

    # Ensure no conflict zone / critical risk manually
    for dest in destinations:
        if dest["geopolitical_risk"] == "critical" or dest["conflict_zone"]:
            raise ValueError("Conflict zone found")
    return destinations

DESTINATION_DATABASE = load_destinations()

# ------------------------------------------------------------------------------
# HELPER FUNCTIONS
def format_eur(value: float) -> str:
    """Format Euro with Italian locale (e.g., €1.250,00)."""
    return f"€{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def get_month_options() -> List[str]:
    """Return list of month names from current month for next 12 months."""
    now = datetime.now()
    months = []
    for i in range(12):
        month_index = (now.month - 1 + i) % 12
        month_name = calendar.month_name[month_index + 1]
        months.append(month_name)
    return months

def calculate_total_cost(dest: Dict, config: Dict) -> float:
    """
    Compute total cost for the trip based on destination and user config.
    config keys: with_flight (bool), board_type ("Full Board" or "Half Board"),
                trip_duration (int), travelers (int)
    """
    with_flight = config["with_flight"]
    board_type = config["board_type"]
    trip_duration = config["trip_duration"]
    travelers = config["travelers"]

    # Flight cost (round trip per person)
    flight = dest["avg_flight_cost_eur"] if with_flight else 0

    # Hotel cost: average for 7 nights, scale to trip_duration
    if board_type == "Full Board 🍽️":
        hotel_7 = dest["avg_hotel_7nights_full_board"]
    else:
        hotel_7 = dest["avg_hotel_7nights_half_board"]
    hotel = (hotel_7 / 7) * trip_duration

    # Local daily expenses
    local = dest["local_daily_expenses_eur"] * trip_duration

    total_per_person = flight + hotel + local
    return total_per_person * travelers

def filter_and_rank(database: List[Dict], user_config: Dict, budget_total: float) -> pd.DataFrame:
    """
    Apply filters, compute smart_score, return sorted DataFrame.
    """
    # Risk tolerance mapping
    risk_map = {
        "Zero Risk (war-free, protest-free)": ["minimal"],
        "Low Risk (minor alerts only)": ["minimal", "low"],
        "Medium Risk (traveler's caution)": ["minimal", "low", "medium"]
    }
    allowed_risks = risk_map[user_config["risk_tolerance"]]

    # Continent filter
    continents = user_config["continent_filter"]
    if "All" not in continents:
        continent_ok = lambda d: d["continent"] in continents
    else:
        continent_ok = lambda d: True

    # Month overlap
    selected_months = user_config["travel_month"]
    if selected_months:
        month_ok = lambda d: any(m in d["best_months"] for m in selected_months)
    else:
        month_ok = lambda d: True

    # Build list
    filtered = []
    for d in database:
        if d["geopolitical_risk"] not in allowed_risks:
            continue
        if not continent_ok(d):
            continue
        if not month_ok(d):
            continue

        total_cost = calculate_total_cost(d, user_config)
        if total_cost <= budget_total:
            risk_level = d["geopolitical_risk"]
            if risk_level == "minimal":
                safety_bonus = 10
            elif risk_level == "low":
                safety_bonus = 8
            elif risk_level == "medium":
                safety_bonus = 5
            else:
                safety_bonus = 0

            budget_fit_score = max(0, 10 - ((total_cost / budget_total) * 10))
            smart_score = (d["value_score"] * 0.4) + (safety_bonus * 0.3) + (budget_fit_score * 0.3)

            filtered.append({
                **d,
                "total_cost_eur": total_cost,
                "smart_score": round(smart_score, 2),
                "safety_bonus": safety_bonus,
                "budget_fit_score": round(budget_fit_score, 2)
            })

    df = pd.DataFrame(filtered)
    if not df.empty:
        df = df.sort_values("smart_score", ascending=False).reset_index(drop=True)
    return df

# ------------------------------------------------------------------------------
# SIDEBAR CONTROLS
st.sidebar.title("✈️ Travel Configuration")

travel_mode = st.sidebar.radio("Travel Mode", ["With Flight ✈️", "Without Flight 🚗🚢"])
board_type = st.sidebar.radio("Board Type", ["Full Board 🍽️", "Half Board 🥗"])
budget_per_person = st.sidebar.slider("Budget per person (€)", 300, 5000, 1200, step=100)
travelers = st.sidebar.number_input("Number of travelers", 1, 10, 2, step=1)

month_options = get_month_options()
default_months = month_options[:3]
travel_month = st.sidebar.multiselect("Travel month(s)", month_options, default=default_months)

trip_duration = st.sidebar.slider("Trip duration (days)", 3, 21, 7, step=1)

continent_filter = st.sidebar.multiselect(
    "Continent",
    ["All", "Europe", "Asia", "Africa", "Americas", "Oceania", "Middle East"],
    default=["All"]
)

risk_tolerance = st.sidebar.selectbox(
    "Risk Tolerance",
    ["Zero Risk (war-free, protest-free)", "Low Risk (minor alerts only)", "Medium Risk (traveler's caution)"]
)

analyze_clicked = st.sidebar.button("🔍 Analyze Destinations", type="primary")

# ------------------------------------------------------------------------------
# MAIN CONTENT
st.title("TravelIQ — Smart Destination Analyzer ✈️")

today = datetime.now().strftime("%d %B %Y")
next_year = (datetime.now().replace(day=1) + pd.DateOffset(months=12)).strftime("%B %Y")
st.info(f"📅 Analysis period: **{today}** → **{next_year}** (next 12 months)")

if not analyze_clicked:
    st.markdown("### 👈 Adjust filters in the sidebar and click **Analyze Destinations**")
    st.stop()

# --- Perform analysis ---
with st.spinner("Analyzing destinations..."):
    user_config = {
        "with_flight": travel_mode == "With Flight ✈️",
        "board_type": board_type,
        "trip_duration": trip_duration,
        "travelers": travelers,
        "risk_tolerance": risk_tolerance,
        "continent_filter": continent_filter,
        "travel_month": travel_month
    }
    budget_total = budget_per_person * travelers
    results_df = filter_and_rank(DESTINATION_DATABASE, user_config, budget_total)

    total_destinations = len(DESTINATION_DATABASE)
    filtered_count = len(results_df)

# Metrics
col1, col2 = st.columns(2)
col1.metric("🌍 Destinations Analyzed", total_destinations)
col2.metric("✅ Matching Your Criteria", filtered_count)

if results_df.empty:
    st.warning("No destinations match your criteria. Try relaxing filters (budget, risk, months, continent).")
    st.stop()

# ------------------------------------------------------------------------------
# RESULTS: TOP DESTINATIONS CARDS
st.subheader(f"🏆 Top {min(9, len(results_df))} Destinations by Smart Score")
top_results = results_df.head(9)

for i in range(0, len(top_results), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        idx = i + j
        if idx < len(top_results):
            dest = top_results.iloc[idx]
            with col:
                # Card with dark background — text always readable
                st.markdown(f"""
                <div class="card">
                    <h2>{dest['flag_emoji']} {dest['destination']}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.write(f"**Smart Score:** {dest['smart_score']}/10")
                st.progress(dest['smart_score'] / 10)

                st.markdown(f"**Total estimated cost:** {format_eur(dest['total_cost_eur'])}")

                with_flight = user_config["with_flight"]
                flight_cost = dest['avg_flight_cost_eur'] if with_flight else 0
                if board_type == "Full Board 🍽️":
                    hotel_7 = dest['avg_hotel_7nights_full_board']
                else:
                    hotel_7 = dest['avg_hotel_7nights_half_board']
                hotel_cost_scaled = (hotel_7 / 7) * trip_duration
                local_cost = dest['local_daily_expenses_eur'] * trip_duration
                total_per_person = flight_cost + hotel_cost_scaled + local_cost
                total_break = total_per_person * travelers

                st.caption(f"✈️ Flight: {format_eur(flight_cost * travelers)}" if with_flight else "✈️ Flight: not included")
                st.caption(f"🏨 Hotel: {format_eur(hotel_cost_scaled * travelers)}")
                st.caption(f"☕ Local: {format_eur(local_cost * travelers)}")

                best_months_list = dest['best_months'][:3]
                badge_str = " ".join([f'<span class="badge-blue">{m}</span>' for m in best_months_list])
                st.markdown(f"**Best months:** {badge_str}", unsafe_allow_html=True)

                risk = dest['geopolitical_risk']
                if risk == "minimal":
                    badge = '<span class="badge-green">✅ Minimal risk</span>'
                elif risk == "low":
                    badge = '<span class="badge-yellow">🟡 Low risk</span>'
                else:
                    badge = '<span class="badge-orange">🟠 Medium risk</span>'
                st.markdown(f"**Risk:** {badge}", unsafe_allow_html=True)

                if dest['active_warnings']:
                    st.warning(f"⚠️ {', '.join(dest['active_warnings'])}")

                st.markdown("**✨ Highlights:**")
                for hl in dest['highlights']:
                    st.markdown(f"- {hl}")

                st.caption(f"🪪 Visa required: {'Yes' if dest['visa_required_for_italians'] else 'No'} | 💱 {dest['currency']} | 🗣️ {dest['language']}")

                with st.expander("📊 Deep Dive"):
                    cost_df = pd.DataFrame({
                        "Item": ["Flight (per person)", "Hotel (per person)", "Local expenses (per person)", "Total per person", "Total for group"],
                        "Cost": [flight_cost, hotel_cost_scaled, local_cost, total_per_person, total_break]
                    })
                    cost_df["Cost (€)"] = cost_df["Cost"].apply(lambda x: format_eur(x))
                    st.table(cost_df[["Item", "Cost (€)"]])
                    st.markdown(f"**Climate in best months:** {dest['climate_in_best_months']}")

# ------------------------------------------------------------------------------
# COMPARISON TABLE
st.subheader("📋 Detailed Comparison Table")
compare_cols = ["destination", "continent", "smart_score", "total_cost_eur", "geopolitical_risk", "best_months", "value_score"]
table_df = results_df[compare_cols].copy()
table_df["total_cost_eur"] = table_df["total_cost_eur"].apply(lambda x: format_eur(x))
table_df.rename(columns={
    "destination": "Destination",
    "continent": "Continent",
    "smart_score": "Smart Score",
    "total_cost_eur": "Total Cost",
    "geopolitical_risk": "Risk Level",
    "best_months": "Best Months",
    "value_score": "Value Score"
}, inplace=True)
st.dataframe(table_df, use_container_width=True)

# ------------------------------------------------------------------------------
# ANALYTICS TABS
tab1, tab2, tab3, tab4 = st.tabs(["📊 Cost Analysis", "🗺️ Geographic Distribution", "📅 Best Travel Calendar", "⚠️ Geopolitical Monitor"])

with tab1:
    top10_cost = results_df.nlargest(10, "total_cost_eur")[["destination", "total_cost_eur"]]
    fig_bar = px.bar(top10_cost, x="destination", y="total_cost_eur", title="Top 10 Destinations by Total Cost",
                     labels={"total_cost_eur": "Total Cost (€)", "destination": ""})
    st.plotly_chart(fig_bar, use_container_width=True)

    scatter_df = results_df.copy()
    scatter_df["safety_label"] = scatter_df["geopolitical_risk"]
    fig_scatter = px.scatter(scatter_df, x="value_score", y="total_cost_eur", size="safety_bonus",
                             color="safety_label", hover_name="destination",
                             title="Value Score vs Total Cost (bubble size = safety)",
                             labels={"value_score": "Value Score (1-10)", "total_cost_eur": "Total Cost (€)"})
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    continent_counts = results_df["continent"].value_counts().reset_index()
    continent_counts.columns = ["continent", "count"]
    fig_pie = px.pie(continent_counts, names="continent", values="count", title="Filtered Destinations by Continent")
    st.plotly_chart(fig_pie, use_container_width=True)

    avg_cost_continent = results_df.groupby("continent")["total_cost_eur"].mean().reset_index()
    avg_cost_continent["total_cost_eur"] = avg_cost_continent["total_cost_eur"].apply(lambda x: format_eur(x))
    st.table(avg_cost_continent.rename(columns={"continent": "Continent", "total_cost_eur": "Average Total Cost"}))

with tab3:
    all_months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    heatmap_data = []
    dest_names = results_df["destination"].tolist()
    for _, row in results_df.iterrows():
        dest_best = row["best_months"]
        row_data = [1 if m in dest_best else 0 for m in all_months]
        heatmap_data.append(row_data)

    fig_heat = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=all_months,
        y=dest_names,
        colorscale=[[0, "#1a1f35"], [1, "#4a90d9"]],
        showscale=False,
        hoverongaps=False
    ))
    fig_heat.update_layout(title="Destination Best Months Heatmap", xaxis_title="Month", yaxis_title="Destination", height=600)
    st.plotly_chart(fig_heat, use_container_width=True)
    st.caption("🔵 Blue = best month for that destination. Your selected months: " + ", ".join(travel_month))

with tab4:
    st.subheader("Risk Overview (Filtered Destinations)")
    risk_table = results_df[["destination", "geopolitical_risk", "active_warnings"]].copy()
    risk_table["geopolitical_risk"] = risk_table["geopolitical_risk"].str.capitalize()
    st.dataframe(risk_table, use_container_width=True)

    st.subheader("🚫 Excluded High-Risk Destinations (always excluded)")
    excluded_list = [
        "Russia", "Ukraine", "Belarus", "Sudan", "Syria", "Yemen", "Myanmar",
        "Haiti", "Gaza/West Bank", "Libya", "Mali", "Burkina Faso", "Niger",
        "North Korea", "Afghanistan", "Iraq", "Somalia"
    ]
    st.markdown(", ".join(excluded_list))
    st.caption("These zones are excluded due to conflict_zone=True or geopolitical_risk='critical'.")
    st.caption(f"*Last simulated update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

# ------------------------------------------------------------------------------
# FOOTER
st.markdown("---")
st.markdown("""
**Disclaimer:** Data based on average market estimates. Always verify current advisories at [viaggiaresicuri.farnesina.it](https://viaggiaresicuri.farnesina.it) and your national foreign ministry.
""")
st.markdown("Powered by **TravelIQ Engine** — Smart Destination Analyzer")
