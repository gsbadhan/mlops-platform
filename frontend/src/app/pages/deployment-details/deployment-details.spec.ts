import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeploymentDetails } from './deployment-details';

describe('DeploymentDetails', () => {
  let component: DeploymentDetails;
  let fixture: ComponentFixture<DeploymentDetails>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DeploymentDetails],
    }).compileComponents();

    fixture = TestBed.createComponent(DeploymentDetails);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
