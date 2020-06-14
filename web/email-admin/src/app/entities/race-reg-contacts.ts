export class RaceRegContacts {

  constructor(
    numberOfRaces: number,
    numberOfClubMembers: number,
    numberOptedIn: number,
  ) {
    this._numberOfRaces = numberOfRaces;
    this._numberOfClubMembers = numberOfClubMembers;
    this._numberOptedIn = numberOptedIn;
  }

  private _numberOfRaces: number;

  get numberOfRaces(): number {
    return this._numberOfRaces;
  }

  set numberOfRaces(numberOfRaces: number) {
    this._numberOfRaces = numberOfRaces;
  }

  private _numberOfClubMembers: number;

  get numberOfClubMembers(): number {
    return this._numberOfClubMembers;
  }

  set numberOfClubMembers(numberOfClubMembers: number) {
    this._numberOfClubMembers = numberOfClubMembers;
  }

  private _numberOptedIn: number;

  get numberOptedIn(): number {
    return this._numberOptedIn;
  }

  set numberOptedIn(numberOptedIn: number) {
    this._numberOptedIn = numberOptedIn;
  }

}
