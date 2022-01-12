import argparse
import ROOT
import glob
import os
import gecorg_test as go
import pandas as pd
import numpy as np
from datetime import date
from ROOT import kOrange, kViolet, kCyan, kGreen, kPink, kAzure, kMagenta, kBlue, kBird
from math import sqrt
import tdrstyle
import CMS_lumi

tdrstyle.setTDRStyle()
CMS_lumi.lumi_13TeV = "101.27 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"

def regionFormatter(regionstr):
    regdict = {'sideband':'sb','signalr':'sr','totalr':'tr'}
    formatted = regdict[regionstr]
    return formatted


if __name__=='__main__':
    #build module objects
    parser = argparse.ArgumentParser()

    #Define parser imputs
    parser.add_argument("-x","--xsec", type=float,help = "desired siganl cross section in fb")
    parser.add_argument("-m","--metcut", type=float,help = "met cut of samples")
    parser.add_argument("-z","--zptcut", type=float,help = "zpt cut of samples")
    parser.add_argument("-j","--hptcut", type=float,help = "hpt cut of samples")
    parser.add_argument("-wp","--btagwp", type=float,help = "btag working point")
    parser.add_argument("-dir","--directory", type=str,help = "date folder with output")
    parser.add_argument("-r","--region",help="region of phase space: totalr,sideband, or signalr")
    parser.add_argument("-y","--year", type=float,help = "year of samples eg. 2017 -> 17")
    parser.add_argument("-s","--syst",type=str,help="systematic string")
    args = parser.parse_args()

    #Get command line parameters
    sig_xsec      = args.xsec
    zptcut        = args.zptcut
    hptcut        = args.hptcut
    metcut        = args.metcut
    btagwp        = args.btagwp
    year          = args.year
    regname       = args.region
    lumi          = 0
    pathplots = args.directory
    systr = args.syst
    
    #Select Plotting years and region
    years = [16,17,18]
    if year:
        years = [int(year)]
    reg = regionFormatter(regname)

    #Gather Input
    bkgs  = go.backgrounds(pathplots,zptcut,hptcut,metcut,btagwp,systr)
    data  = go.run2(pathplots,zptcut,hptcut,metcut,btagwp,systr)
    #sigs = go.
    dynorm = 1
    #if len(years) >= 2:#dynorms only matter for composite years
    #    dynorm = np.load(pathplots+'/Run2_2017_2018_dynormalization_'+systr+'_signalblind_Zptcut'+zptcut+'_Hptcut'+hptcut+'_metcut'+metcut+'_btagwp'+btagwp+'.npy')[0]

    #Include data?

    #Colors and Naming
    bkgnames = ["DYJetsToLL","TT","WZTo2L2Q","ZZTo2L2Q"]
    bkgcols  = go.colsFromPalette(bkgnames,ROOT.kLake)

    #Gather plots
    testyear = years[0]#picks first year in list, so desired year if only one
    testfile = bkgs.bkgs["DYJetsToLL"][testyear]["sb"][0][0]#stacked plots should always have DY
    testtfile = ROOT.TFile(testfile)
    keys = testtfile.GetListOfKeys()

    #names and param. To Do: expand to include plot limits for linear scale
    titles = {
        "h_z_pt":"Z p_{T}",
        "h_z_eta":"\eta_{Z}",
        "h_z_phi":"\phi_{Z}",
        "h_z_phiw":"\phi_{Z}",
        "h_z_m":"m_{Z}",
        "h_h_pt":"Higgs p_{T}",
        "h_h_eta":"\eta_{Higss}",
        "h_h_phi":"\phi_{Higgs}",
        "h_h_phiw":"\phi_{Higgs}",
        "h_h_m":"m_{h}",
        "h_h_sd":"Higgs Soft Drop Mass",
        "h_met":"p_{T}^{miss}",
        "h_met_phi":"\phi p_{T}^{miss}",
        "h_met_phiw":"\phi p_{T}^{miss}",
        "h_zp_jigm":"Jigsaw Mass Estimator Z'",
        "h_nd_jigm":"Jigsaw Mass Estimator ND",
        "h_ns_jigm":"Jigsaw Mass Estimator NS",
        "h_weights":"event weights",
        "h_btag":"btag operating point",
        "h_dphi_zh":"\Delta\phi_{ZH}",
        "h_dphi_zmet":"\Delta\phi_{ZMET}",
        "h_dphi_hmet":"\Delta\phi_{HMET}",
        "h_dr_zh":"\Delta R(ZH)",
        "h_dr_lmuh":"\Delta R(lmu,H)",
        "h_dr_slmuh":"\Delta R(slmu,H)",
        "h_dr_slmulmu":"\Delta R(slmu,lmu)",
    }


    #make the plots
    for key in keys:
        hname = key.GetName()
        
        #Make holder histograms
        h = testtfile.Get(hname)
        if (not isinstance(h,ROOT.TH1)) or ('h_weights' in hname):
            continue
        empty = h.Clone()
        empty.Reset("ICESM")#creates an empty hist with same structure
        empty1 = empty.Clone()
        empty2 = empty.Clone()
        empty3 = empty.Clone()
        empty4 = empty.Clone()
        empty5 = empty.Clone()
        empty6 = empty.Clone()
        empty7 = empty.Clone()
        empty8 = empty.Clone()
        empty9 = empty.Clone()

        #Gather histograms
        hdat = data.getAddedHist(empty1,reg,hname,years = years)
        hdy  = bkgs.getAddedHist(empty2,"DYJetsToLL",reg,hname,years = years)
        htt  = bkgs.getAddedHist(empty3,"TT",reg,hname,years = years)
        hzz  = bkgs.getAddedHist(empty4,"ZZTo2L2Q",reg,hname,years = years)
        hwz  = bkgs.getAddedHist(empty5,"WZTo2L2Q",reg,hname,years = years)

        hdy.Scale(dynorm)
        hdy.SetFillColor(bkgcols[0])
        hdy.SetLineColor(bkgcols[0])
        htt.SetFillColor(bkgcols[1])
        htt.SetLineColor(bkgcols[1])
        hwz.SetFillColor(bkgcols[2])
        hwz.SetLineColor(bkgcols[2])
        hzz.SetFillColor(bkgcols[3])
        hzz.SetLineColor(bkgcols[3])

        
