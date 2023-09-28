from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Head(BaseModel):
    status: str
    data: Dict[str, Any]


class Regular(BaseModel):
    storeSearchEnabled: bool
    storePickupLabel: str
    storeSelectionEnabled: bool
    storePickupQuote: str
    storePickupQuote2_0: str
    storePickupLinkText: str
    storePickupProductTitle: str


class MessageTypes(BaseModel):
    regular: Regular


class MU6Q3VCA(BaseModel):
    storePickEligible: bool
    pickupSearchQuote: str
    partNumber: str
    purchaseOption: str
    ctoOptions: str
    pickupDisplay: str
    pickupType: str
    messageTypes: MessageTypes


class PartsAvailability(BaseModel):
    MU6Q3VC_A: MU6Q3VCA = Field(..., alias='MU6Q3VC/A')


class Address(BaseModel):
    address: str
    address3: Any
    address2: str
    postalCode: str


class Hour(BaseModel):
    storeTimings: str
    storeDays: str


class StoreHours(BaseModel):
    storeHoursText: str
    bopisPickupDays: str
    bopisPickupHours: str
    hours: List[Hour]


class Address1(BaseModel):
    city: str
    companyName: str
    countryCode: str
    county: Any
    district: Any
    geoCode: Any
    label: Any
    languageCode: str
    mailStop: Any
    postalCode: str
    province: Any
    state: str
    street: str
    street2: Any
    street3: Any
    suburb: Any
    type: str
    addrSourceType: Any
    outsideCityFlag: Any
    daytimePhoneAreaCode: Any
    eveningPhoneAreaCode: Any
    daytimePhone: str
    fullPhoneNumber: Any
    eveningPhone: Any
    emailAddress: Any
    firstName: Any
    lastName: Any
    suffix: Any
    lastNamePhonetic: Any
    firstNamePhonetic: Any
    title: Any
    bundlePaymentAddress: bool
    businessAddress: bool
    uuid: str
    mobilePhone: Any
    mobilePhoneAreaCode: Any
    cityStateZip: Any
    daytimePhoneSelected: bool
    middleName: Any
    residenceStatus: Any
    moveInDate: Any
    subscriberId: Any
    locationType: Any
    carrierCode: Any
    metadata: Dict[str, Any]
    verificationState: str
    expiration: Any
    markForDeletion: bool
    correctionResult: Any
    fullDaytimePhone: str
    fullEveningPhone: Any
    twoLineAddress: str
    addressVerified: bool
    primaryAddress: bool


class StoreHour(BaseModel):
    storeDays: str
    voStoreDays: Any
    storeTimings: str


class TypeCoordinate(BaseModel):
    lat: float
    lon: float


class TypeDirection(BaseModel):
    directionByLocale: Any


class TypeMeetupLocation(BaseModel):
    meetingLocationByLocale: Any


class INSTORE(BaseModel):
    type: str
    typeCoordinate: TypeCoordinate
    typeDirection: TypeDirection
    typeMeetupLocation: TypeMeetupLocation
    services: List[str]


class StorePickupMethodByType(BaseModel):
    INSTORE: INSTORE


class RetailStore(BaseModel):
    storeNumber: str
    storeUniqueId: str
    name: str
    storeTypeKey: str
    storeSubTypeKey: str
    storeType: str
    phoneNumber: str
    email: str
    carrierCode: Any
    locationType: Any
    latitude: float
    longitude: float
    address: Address1
    urlKey: Any
    directionsUrl: Any
    storeImageUrl: str
    makeReservationUrl: str
    hoursAndInfoUrl: str
    storeHours: List[StoreHour]
    storeHolidays: List
    secureStoreImageUrl: str
    distance: float
    distanceUnit: str
    distanceWithUnit: str
    timezone: str
    storeIsActive: bool
    lastUpdated: float
    lastFetched: int
    dateStamp: str
    distanceSeparator: str
    nextAvailableDate: Any
    storeHolidayLookAheadWindow: int
    driveDistanceWithUnit: Any
    driveDistanceInMeters: Any
    dynamicAttributes: Dict[str, Any]
    storePickupMethodByType: StorePickupMethodByType
    storeTimings: Any
    availableNow: bool


class PickupOption(BaseModel):
    pickupOptionTitle: str
    pickupOptionDescription: str
    index: int


class PickupOptionsDetails(BaseModel):
    whatToExpectAtPickup: str
    comparePickupOptionsLink: str
    pickupOptions: List[PickupOption]


class Store(BaseModel):
    storeEmail: str
    storeName: str
    reservationUrl: str
    makeReservationUrl: str
    state: str
    storeImageUrl: str
    country: str
    city: str
    storeNumber: str
    partsAvailability: PartsAvailability
    phoneNumber: str
    pickupTypeAvailabilityText: str
    address: Address
    hoursUrl: str
    storeHours: StoreHours
    storelatitude: float
    storelongitude: float
    storedistance: float
    storeDistanceWithUnit: str
    storeDistanceVoText: str
    retailStore: RetailStore
    storelistnumber: int
    storeListNumber: int
    pickupOptionsDetails: PickupOptionsDetails
    rank: int


class Availability(BaseModel):
    isComingSoon: bool


class Body(BaseModel):
    stores: List[Store]
    overlayInitiatedFromWarmStart: bool
    viewMoreHoursLinkText: str
    storesCount: str
    little: bool
    location: str
    notAvailableNearby: str
    notAvailableNearOneStore: str
    warmDudeWithAPU: bool
    viewMoreHoursVoText: str
    availability: Availability
    viewDetailsText: str
    availabilityStores: str
    legendLabelText: str
    filteredTopStore: bool


class PickupData(BaseModel):
    head: Head
    body: Body
