#ifdef __CLING__
R__LOAD_LIBRARY(libDelphes)
#include "classes/DelphesClasses.h"
#include "external/ExRootAnalysis/ExRootTreeReader.h"
#endif

#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TCanvas.h>
#include <TLorentzVector.h>




void pp2ee(const char *inputFile){
gSystem->Load("libDelphes");

  // Create chain of root trees
  TChain chain("Delphes");
  chain.Add(inputFile);

  // Create object of class ExRootTreeReader
  ExRootTreeReader *treeReader = new ExRootTreeReader(&chain);
  Long64_t numberOfEntries = treeReader->GetEntries();

  // Get pointers to branches used in this analysis
  TClonesArray *branchJet = treeReader->UseBranch("Jet");
  TClonesArray *branchElectron = treeReader->UseBranch("Electron");
  TClonesArray *branchEvent = treeReader->UseBranch("Event");

  // Book histograms
  TH1 *histJetPT = new TH1F("jet_pt", "jet P_{T}", 100, 0.0, 100.0);
  TH1 *histMass = new TH1F("mass", "M_{inv}(e_{1}, e_{2})", 100, 40.0, 140.0);

  // Loop over all events
  for(Int_t entry = 0; entry < numberOfEntries; ++entry)
  {
    // Load selected branches with data from specified event
    treeReader->ReadEntry(entry);


    //HepMCEvent *event = (HepMCEvent*) branchEvent -> At(0);
    //LHEFEvent *event = (LHEFEvent*) branchEvent -> At(0);
    //Float_t weight = event->Weight;

    // If event contains at least 1 jet
    if(branchJet->GetEntries() > 0)
	{
      // Take first jet
      Jet *jet = (Jet*) branchJet->At(0);

      // Plot jet transverse momentum
      histJetPT->Fill(jet->PT);

      // Print jet transverse momentum
      cout << "Jet pt: "<<jet->PT << endl;
    }

    Electron *elec1, *elec2;

    // If event contains at least 2 electrons
    if(branchElectron->GetEntries() > 1)
    {
      // Take first two electrons
      elec1 = (Electron *) branchElectron->At(0);
      elec2 = (Electron *) branchElectron->At(1);

      // Plot their invariant mass
      histMass->Fill(((elec1->P4()) + (elec2->P4())).M());
    }
  }

  // Show resulting histograms
  //histJetPT->Draw();
  histMass->Draw();







/*
	TFile* file = new TFile("/home/waldeinsamkeit/work/MG5_aMC_v2_9_16/pp2eeAll/Events/run_01/tag_1_delphes_events.root", "READ");
	TTree* tree = (TTree*)file->Get("Delphes");

	TH1F* invariantMassHist = new TH1F("invariantMassHist", "Invariant Mass Histogram", 100, 0, 200);

	Int_t Enum;	
	Float_t Ept, Eeta, Ephi;
	tree->SetBranchAddress("Electron", &Enum);
	tree->SetBranchAddress("Electron.PT", &Ept);
	tree->SetBranchAddress("Electron.Eta", &Eeta);
	tree->SetBranchAddress("Electron.Phi", &Ephi);

	Long64_t nEntries = tree->GetEntries();
	for (Long64_t i = 0; i < nEntries; ++i) {
    		tree->GetEntry(i);
    		invariantMassHist->Fill(Ept);
	}	

 	TCanvas* canvas = new TCanvas("canvas", "Invariant Mass Histogram", 800, 600);
	invariantMassHist->Draw();
	canvas->SaveAs("invariantMassHisttest.png");
*/
}
