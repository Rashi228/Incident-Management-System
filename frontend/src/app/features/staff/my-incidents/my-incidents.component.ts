import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { IncidentService } from '../../../core/services/incident.service';
import { Incident } from '../../../models/incident.model';
import { BadgeComponent } from '../../../shared/components/badge/badge.component';

@Component({
  selector: 'app-my-incidents',
  standalone: true,
  imports: [CommonModule, DatePipe, RouterLink, BadgeComponent],
  templateUrl: './my-incidents.component.html',
  styleUrl: './my-incidents.component.css'
})
export class MyIncidentsComponent implements OnInit {
  incidents: Incident[] = [];
  loading = true;

  constructor(private incidentService: IncidentService) {}

  ngOnInit() {
    this.incidentService.getAll().subscribe({
      next: (data) => { this.incidents = data; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }
}
