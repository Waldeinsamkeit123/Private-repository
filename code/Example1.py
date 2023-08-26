#!/usr/bin/env python

import sys

import ROOT

try:
  input = raw_input
except:
  pass

if len(sys.argv) < 2:
  print(" Usage: Example1.py input_file")
  sys.exit(1)

ROOT.gSystem.Load("libDelphes")

try:
  ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
  ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
  pass

inputFile1 = sys.argv[1]
inputFile2 = sys.argv[2]
inputFile3 = sys.argv[3]

print("pp2mm",sys.argv[1])
print("pp2z2mm",sys.argv[2])
print("pp2mmFbz",sys.argv[3])

# Create chain of root trees
chain1 = ROOT.TChain("Delphes")
chain1.Add(inputFile1)
chain2 = ROOT.TChain("Delphes")
chain2.Add(inputFile2)
chain3 = ROOT.TChain("Delphes")
chain3.Add(inputFile3)

# Create object of class ExRootTreeReader
treeReader1 = ROOT.ExRootTreeReader(chain1)
numberOfEntries1 = treeReader1.GetEntries()
treeReader2 = ROOT.ExRootTreeReader(chain2)
numberOfEntries2 = treeReader2.GetEntries()
treeReader3 = ROOT.ExRootTreeReader(chain3)
numberOfEntries3 = treeReader3.GetEntries()

# Get pointers to branches used in this analysis
# branchJet = treeReader.UseBranch("Jet")
branchMuon1 = treeReader1.UseBranch("Muon")
branchMuon2 = treeReader2.UseBranch("Muon")
branchMuon3 = treeReader3.UseBranch("Muon")

# Book histograms
# histJetPT = ROOT.TH1F("jet_pt", "jet P_{T}", 100, 0.0, 100.0)
histMass1 = ROOT.TH1F("mass,pp2mm", "M_{inv}(mu_{1}, mu_{2})", 100, 40.0, 140.0)
histMass2 = ROOT.TH1F("mass,pp2z2mm", "M_{inv}(mu_{1}, mu_{2})", 100, 40.0, 140.0)
histMass3 = ROOT.TH1F("mass,pp2mmFbz", "M_{inv}(mu_{1}, mu_{2})", 100, 40.0, 140.0)
histMass1.SetLineColor(ROOT.kRed)
histMass2.SetLineColor(ROOT.kBlue)
histMass3.SetLineColor(ROOT.kBlack)

# Loop over all events
for entry in range(0, numberOfEntries1):
  # Load selected branches with data from specified event
  treeReader1.ReadEntry(entry)

  # If event contains at least 1 jet
#  if branchJet.GetEntries() > 0:
    # Take first jet
#    jet = branchJet.At(0)

    # Plot jet transverse momentum
#    histJetPT.Fill(jet.PT)

    # Print jet transverse momentum
#    print(jet.PT)

  # If event contains at least 2 electrons
  if branchMuon1.GetEntries() > 1:
    # Take first two electrons
    mu11 = branchMuon1.At(0)
    mu12 = branchMuon1.At(1)

    # Plot their invariant mass
    histMass1.Fill(((mu11.P4()) + (mu12.P4())).M())

for entry in range(0, numberOfEntries2):
  # Load selected branches with data from specified event
  treeReader2.ReadEntry(entry)

  # If event contains at least 1 jet
#  if branchJet.GetEntries() > 0:
    # Take first jet
#    jet = branchJet.At(0)

    # Plot jet transverse momentum
#    histJetPT.Fill(jet.PT)

    # Print jet transverse momentum
#    print(jet.PT)

  # If event contains at least 2 electrons
  if branchMuon2.GetEntries() > 1:
    # Take first two electrons
    mu21 = branchMuon2.At(0)
    mu22 = branchMuon2.At(1)

    # Plot their invariant mass
    histMass2.Fill(((mu21.P4()) + (mu22.P4())).M())

for entry in range(0, numberOfEntries3):
  # Load selected branches with data from specified event
  treeReader3.ReadEntry(entry)

  # If event contains at least 1 jet
#  if branchJet.GetEntries() > 0:
    # Take first jet
#    jet = branchJet.At(0)

    # Plot jet transverse momentum
#    histJetPT.Fill(jet.PT)

    # Print jet transverse momentum
#    print(jet.PT)

  # If event contains at least 2 electrons
  if branchMuon3.GetEntries() > 1:
    # Take first two electrons
    mu31 = branchMuon3.At(0)
    mu32 = branchMuon3.At(1)

    # Plot their invariant mass
    histMass3.Fill(((mu31.P4()) + (mu32.P4())).M())

# Show resulting histograms
canvas = ROOT.TCanvas("canvas", "Multiple Processes", 800, 600)

#histJetPT.Draw()
histMass1.Draw()
histMass2.Draw("same")
histMass3.Draw("same")

legend = ROOT.TLegend(0.65, 0.65, 0.8, 0.8)  # 设置图例的位置
legend.AddEntry(histMass1, "pp2mm", "l")
legend.AddEntry(histMass2, "pp2z2mm", "l")
legend.AddEntry(histMass3, "pp2mmFbz", "l")
legend.Draw()

yaxis = histMass1.GetYaxis()
yaxis.SetRangeUser(0, histMass1.GetMaximum() * 1.1)

input("Press Enter to continue...")
