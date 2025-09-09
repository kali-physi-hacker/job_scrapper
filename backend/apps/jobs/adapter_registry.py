from typing import Dict, Any
from .adapters.base import JobAdapterBase
from .adapters.greenhouse import GreenhouseAdapter
from .adapters.lever import LeverAdapter
from .adapters.smartrecruiters import SmartRecruitersAdapter
from .adapters.recruitee import RecruiteeAdapter
from .adapters.workable import WorkableAdapter
from .adapters.ashby import AshbyAdapter
from .adapters.workday import WorkdayAdapter
from .adapters.breezy import BreezyAdapter
from .adapters.teamtailor import TeamtailorAdapter
from .adapters.icims import ICIMSAdapter


ADAPTERS = {
    GreenhouseAdapter.key: GreenhouseAdapter,
    LeverAdapter.key: LeverAdapter,
    SmartRecruitersAdapter.key: SmartRecruitersAdapter,
    RecruiteeAdapter.key: RecruiteeAdapter,
    WorkableAdapter.key: WorkableAdapter,
    AshbyAdapter.key: AshbyAdapter,
    WorkdayAdapter.key: WorkdayAdapter,
    BreezyAdapter.key: BreezyAdapter,
    TeamtailorAdapter.key: TeamtailorAdapter,
    ICIMSAdapter.key: ICIMSAdapter,
}


def get_adapter(key: str, config: Dict[str, Any] | None = None) -> JobAdapterBase:
    cls = ADAPTERS.get(key)
    if not cls:
        return JobAdapterBase(config)  # type: ignore[call-arg]
    return cls(config)
