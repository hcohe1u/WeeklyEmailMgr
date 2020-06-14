import { Component, OnInit, AfterViewInit } from '@angular/core';
import { ClubContacts } from './entities/club-contacts';
import { RaceRegContacts } from './entities/race-reg-contacts';
import { Emails } from './entities/emails';
import { FormControl } from '@angular/forms';
import { EmailManagerService } from './services/email-manager.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, AfterViewInit {

  clubContacts: ClubContacts;
  raceRegContacts: RaceRegContacts;
  emails: Emails;

  constructor(private emailManagerService: EmailManagerService) {}

  title = 'AARC Email Manager';

  ngOnInit() {
    this.refreshClubContacts();
    this.refreshRaceRegContacts();
    this.refreshEmails();
  }

  ngAfterViewInit() {
  }

  refreshClubContacts() {
    this.emailManagerService.getClubContacts()
    .subscribe((data: ClubContacts) => this.clubContacts = data,
        error => console.log('Error returned', error));
  }

  refreshRaceRegContacts() {
    this.emailManagerService.getRaceRegContacts()
    .subscribe((data: RaceRegContacts) => this.raceRegContacts = data,
        error => console.log('Error returned', error));
  }

  refreshEmails() {
    this.emailManagerService.getEmails()
    .subscribe((data: Emails) => this.emails = data,
        error => console.log('Error returned', error));
  }

}


