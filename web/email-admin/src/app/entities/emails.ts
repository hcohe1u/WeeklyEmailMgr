export class Emails {

  constructor(
    numberOfEmailsRelayed: number,
    dateOfLastEmailRelayed: string,
    dateOfRelayed: string,
    numberOfEmailsSent: number,
  ) {
    this._numberOfEmailsRelayed = numberOfEmailsRelayed;
    this._dateOfLastEmailRelayed = dateOfLastEmailRelayed;
    this._dateOfRelayed = dateOfRelayed;
    this._numberOfEmailsSent = numberOfEmailsSent;
  }

  private _numberOfEmailsRelayed: number;

  get numberOfEmailsRelayed(): number {
    return this._numberOfEmailsRelayed;
  }

  set numberOfEmailsRelayed(numberOfEmailsRelayed: number) {
    this._numberOfEmailsRelayed = numberOfEmailsRelayed;
  }

  private _dateOfLastEmailRelayed: string;

  get dateOfLastEmailRelayed(): string {
    return this._dateOfLastEmailRelayed;
  }

  set dateOfLastEmailRelayed(dateOfLastEmailRelayed: string) {
    this._dateOfLastEmailRelayed = dateOfLastEmailRelayed;
  }

  private _dateOfRelayed: string;

  get dateOfRelayed(): string {
    return this._dateOfRelayed;
  }

  set dateOfRelayed(dateOfRelayed: string) {
    this._dateOfRelayed = dateOfRelayed;
  }

  private _numberOfEmailsSent: number;

  get numberOfEmailsSent(): number {
    return this._numberOfEmailsSent;
  }

  set numberOfEmailsSent(xxx: number) {
    this._numberOfEmailsSent = xxx;
  }

}
