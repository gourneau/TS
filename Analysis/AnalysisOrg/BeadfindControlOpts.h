/* Copyright (C) 2010 Ion Torrent Systems, Inc. All Rights Reserved */
#ifndef BEADFINDCONTROLOPTS_H
#define BEADFINDCONTROLOPTS_H
#include <vector>
#include <string>
#include <map>
#include <set>
#include "Region.h"
#include "IonVersion.h"
#include "Utils.h"

class BeadfindControlOpts{
  public:
    double bfMinLiveRatio;
    double bfMinLiveLibSnr;
    double bfMinLiveTfSnr;
    double bfTfFilterQuantile;
    double bfLibFilterQuantile;
    int skipBeadfindSdRecover;
    int beadfindThumbnail; // Is this a thumbnail chip where we need to skip smoothing across regions?
    int beadfindLagOneFilt;
    char *beadMaskFile;
    int maskFileCategorized;
    char bfFileBase[MAX_PATH_LENGTH];
    char preRunbfFileBase[MAX_PATH_LENGTH];
    int noduds;
    int bfOutputDebug;
    std::string beadfindType;
    std::string bfType; // signal or buffer
    std::string bfDat;
    std::string bfBgDat;
    bool SINGLEBF;
    int BF_ADVANCED;
    bool useSignalReference;
    void DefaultBeadfindControl();
    ~BeadfindControlOpts();
};


#endif // BEADFINDCONTROLOPTS_H
