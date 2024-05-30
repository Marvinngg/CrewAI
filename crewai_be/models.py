from typing import List, Optional
from pydantic import BaseModel


class NamedUrl(BaseModel):
    name: str
    url: str


class PositionInfo(BaseModel):
    company: str
    position: str
    name: str
    blog_articles_urls: List[str]
    youtube_interviews_urls: List[NamedUrl]


class PositionInfoList(BaseModel):
    positions: List[PositionInfo]


class FlightInfo(BaseModel):
    airline: str
    cost: float
    url: str


class WeatherForecast(BaseModel):
    date: str
    forecast: str
    temperature_high: float
    temperature_low: float


class Attraction(BaseModel):
    name: str
    description: str
    url: Optional[str]


class CityReport(BaseModel):
    chosen_city: str
    flight_costs: List[FlightInfo]
    weather_forecast: List[WeatherForecast]
    attractions: List[Attraction]


class CityGuide(BaseModel):
    key_attractions: List[str]
    local_customs: str
    special_events: str
    daily_recommendations: List[str]
    hidden_gems: List[str]
    cultural_hotspots: List[str]
    must_visit_landmarks: List[str]
    weather_forecast: str
    high_level_costs: str


class DailyPlan(BaseModel):
    day: int
    activities: List[str]
    hotel: str
    restaurants: List[str]
    weather_forecast: str
    packing_suggestions: List[str]
    budget_breakdown: str


class TravelItinerary(BaseModel):
    travel_itinerary: List[DailyPlan]


class CityGuideOutput(BaseModel):
    city_guide: CityGuide


class TravelPlanOutput(BaseModel):
    travel_plan: TravelItinerary
class MacroEconomicData(BaseModel):
    gdp: float
    inflation_rate: float
    unemployment_rate: float
    interest_rate: float
    trade_balance: float
    fiscal_deficit: float


class MacroEconomicReport(BaseModel):
    country: str
    data: MacroEconomicData
    analysis: str
class IndustryData(BaseModel):
    market_size: float
    growth_rate: float
    key_players: List[str]
    competitive_landscape: str
    regulatory_environment: str
    technological_advancements: str


class IndustryReport(BaseModel):
    industry_name: str
    data: IndustryData
    analysis: str
class FinancialReport(BaseModel):
    year: int
    revenue: float
    profit: float
    assets: float
    liabilities: float


class MarketData(BaseModel):
    market_share: float
    competitors: List[str]
    growth_rate: float


class BusinessOperations(BaseModel):
    business_model: str
    products_services: List[str]
    customer_base: str
    sales_channels: List[str]


class StrategicPositioning(BaseModel):
    strategy: str
    goals: str
    core_competencies: str
    market_positioning: str


class CompanyAnalysisData(BaseModel):
    financial_reports: List[FinancialReport]
    market_data: MarketData
    business_operations: BusinessOperations
    strategic_positioning: StrategicPositioning


class CompanyReport(BaseModel):
    company_name: str
    data: CompanyAnalysisData
    analysis: str
