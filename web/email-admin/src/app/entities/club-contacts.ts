export class ClubContacts {

  constructor(
    numberOfEntrants: number,
    numberOfClubMembers: number,
    numberOfContacts: number,
  ) {
    this._numberOfEntrants = numberOfEntrants;
    this._numberOfClubMembers = numberOfClubMembers;
    this._numberOfContacts = numberOfContacts;
  }

  private _numberOfEntrants: number;

  get numberOfEntrants(): number {
    return this._numberOfEntrants;
  }

  set numberOfEntrants(numberOfEntrants: number) {
    this._numberOfEntrants = numberOfEntrants;
  }

  private _numberOfClubMembers: number;

  get numberOfClubMembers(): number {
    console.log(`numberOfClubMembers = {this._numberOfClubMembers}`);
    return this._numberOfClubMembers;
  }

  set numberOfClubMembers(numberOfClubMembers: number) {
    this._numberOfClubMembers = numberOfClubMembers;
  }

  private _numberOfContacts: number;

  get numberOfContacts(): number {
    return this._numberOfContacts;
  }

  set numberOfContacts(numberOfContacts: number) {
    this._numberOfContacts = numberOfContacts;
  }

}
