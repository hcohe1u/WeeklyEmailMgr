import { ClubContacts } from '../entities/club-contacts';
import { RaceRegContacts } from '../entities/race-reg-contacts';
import { Emails } from '../entities/emails';
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, Observer, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators'
const URL_PREFIX = 'https://api.exemplys.com/weekly-emails/';


@Injectable({
  providedIn: 'root'
})
export class EmailManagerService {

  errorHandler = {
    log: (message, error) => console.log(message, error),
    alertFriendlyInfo: (message, observer: Observer<any>) => observer.error(message)
  };

  constructor(private http: HttpClient) { }

  getClubContacts(): Observable<ClubContacts> {
    return this.http.get<ClubContacts>(`${URL_PREFIX}/club-contacts`)
    .pipe(
      catchError( (error: HttpErrorResponse) => {
        this.errorHandler.log('Error while getting club contacts', error);
        return throwError('Error while getting club contacts');
      }));
  }
  getRaceRegContacts(): Observable<RaceRegContacts> {
    return this.http.get<RaceRegContacts>(`${URL_PREFIX}/race-reg-contacts`)
    .pipe(
      catchError( (error: HttpErrorResponse) => {
        this.errorHandler.log('Error while getting race reg contacts', error);
        return throwError('Error while getting race reg contacts');
      }));
  }
  getEmails(): Observable<Emails> {
    return this.http.get<Emails>(`${URL_PREFIX}/emails`)
    .pipe(
      catchError( (error: HttpErrorResponse) => {
        this.errorHandler.log('Error while getting emails', error);
        return throwError('Error while getting emails');
      }));
  }

}



