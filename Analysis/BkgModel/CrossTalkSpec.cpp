/* Copyright (C) 2010 Ion Torrent Systems, Inc. All Rights Reserved */
#include "CrossTalkSpec.h"

// set up cross-talk information in a clean way

void CrossTalkSpecification::Allocate(int size)
{
    DeAllocate();  // in case we had something here before
    nei_affected = size;
    cx = new int[size];
    cy = new int[size];
    mix = new float[size];
    delay = new float[size];
    //my new goofy parameters
    tau_top = new float[size];
    tau_fluid = new float[size];
    multiplier = new float[size];
}

void CrossTalkSpecification::DeAllocate()
{
    if (cx!=NULL)
        delete[] cx;
    if (cy!=NULL)
        delete[] cy;
    if (mix !=NULL)
        delete[] mix;
    if (delay !=NULL)
        delete[] delay;
    if (tau_top!=NULL)
        delete[] tau_top;
    if (tau_fluid!=NULL)
        delete[] tau_fluid;
    if (multiplier!=NULL)
        delete[] multiplier;

    cx=NULL;
    cy= NULL;
    mix = NULL;
    delay = NULL;

    tau_top = NULL;
    tau_fluid = NULL;
    multiplier = NULL;

}

CrossTalkSpecification::CrossTalkSpecification()
{
    cx = NULL;
    cy = NULL;
    mix = NULL;
    delay = NULL;

    tau_top = NULL;
    tau_fluid = NULL;
    multiplier = NULL;


    nei_affected = 0;
    tau_bulk = -1.0;
    cbulk = 1;
    nscale = 0;
    hex_packed = false;
    do_xtalk_correction = true;
}

CrossTalkSpecification::~CrossTalkSpecification()
{
    DeAllocate();
}

// this is of unknown utility
void CrossTalkSpecification::SetStandardGrid()
{
    hex_packed = false;
    Allocate(5); // how many neighbors are significant
    int ndx=0;
    cx[ndx] = -1;
    cy[ndx] = 0;
    delay[ndx] = 3.0;
    mix[ndx] = 1.0;
    ndx++;
    cx[ndx] = 1, cy[ndx] = 1;
    delay[ndx] = 3.0;
    mix[ndx] = 1.0;
    ndx++;
    cx[ndx] = 0;
    cy[ndx] = -1;
    delay[ndx] = 3.0;
    mix[ndx] = 1.0;
    ndx++;
    cx[ndx] = 0;
    cy[ndx] = 1;
    delay[ndx] = 3.0;
    mix[ndx] = 0.7;
    ndx++;
    cx[ndx] = 1;
    cy[ndx] = 1;
    delay[ndx] = 6.0;
    mix[ndx] = 0.8;
    ndx++;
    tau_bulk = 14.0;
    cbulk = 45;
    nscale = 4.0;
}

void CrossTalkSpecification::SetNewQuadGrid()
{
    //printf("Quad Grid set\n");
    hex_packed = false;
    //Allocate(8); // how many neighbors are significant
    Allocate(5); // after commenting out zero neighbors
    // left/right
    int ndx = 0;
    cx[ndx] = -1;
    cy[ndx] = 0;
    tau_top[ndx] = 3;
    tau_fluid[ndx] = 7;
    multiplier[ndx] = 0.02;
    ndx++;// reduced because downstream
    cx[ndx] = 1,  cy[ndx] = 0;
    tau_top[ndx] = 3;
    tau_fluid[ndx] = 7;
    multiplier[ndx] = 0.03;
    ndx++;
    // phase of hex grid shifts these two entities
    // up
    //cx[ndx] = -1; cy[ndx] = 1;  tau_top[ndx] = 3; tau_fluid[ndx] = 7; multiplier[ndx] = 0.00; ndx++;
    cx[ndx] = 0;
    cy[ndx] = 1;
    tau_top[ndx] = 3;
    tau_fluid[ndx] = 7;
    multiplier[ndx] = 0.03;
    ndx++;
    cx[ndx] = 1;
    cy[ndx] = 1;
    tau_top[ndx] = 3;
    tau_fluid[ndx] = 7;
    multiplier[ndx] = 0.02;
    ndx++; // upstream towards inlet neighbor, reduced because diagonal
    // down
    //cx[ndx] = -1; cy[ndx] = -1;  tau_top[ndx] = 3; tau_fluid[ndx] = 7; multiplier[ndx] = 0.00; ndx++;
    cx[ndx] = 0;
    cy[ndx] = -1;
    tau_top[ndx] = 3;
    tau_fluid[ndx] = 7;
    multiplier[ndx] = 0.02;
    ndx++; // reduced because downstream
    //cx[ndx] = 1; cy[ndx] = -1; tau_top[ndx] = 3; tau_fluid[ndx] = 7; multiplier[ndx] = 0.00; ndx++;

}

// this is fictitious and has never been used
// because of course we don't tell the analysis program that the chip is a 318
// or at least not the background model
void CrossTalkSpecification::SetHexGrid()
{
    hex_packed = true;
    Allocate(6); // how many neighbors are significant
    int ndx = 0;
    cx[ndx] = -1;
    cy[ndx] = 0;
    delay[ndx] = 3.0;
    mix[ndx] = 1.0;
    ndx++;
    cx[ndx] = 1;
    cy[ndx] = 1;
    delay[ndx] = 3.0;
    mix[ndx] = 1.0;
    ndx++;
    cx[ndx] = 0;
    cy[ndx] = -1;
    delay[ndx] = 3.0;
    mix[ndx] = 1.0;
    ndx++;
    cx[ndx] = 0;
    cy[ndx] = 1;
    delay[ndx] = 3.0;
    mix[ndx] = 0.7;
    ndx++;
    cx[ndx] = -1;
    cy[ndx] = 1;
    delay[ndx] = 6.0;
    mix[ndx] = 0.6;
    ndx++;
    cx[ndx] = -1;
    cy[ndx] = -1;
    delay[ndx] = 6.0;
    mix[ndx]= 0.6;
    ndx++;
    tau_bulk = 14.0;
    cbulk = 35;
    nscale = 4.0;
}

void CrossTalkSpecification::SetNewHexGrid()
{
    hex_packed = true;
    Allocate(6);
    int ndx = 0;
    // left/right
    cx[ndx] = -1;
    cy[ndx] = 0;
    tau_top[ndx] = 5;
    tau_fluid[ndx] = 15;
    multiplier[ndx] = 0.01;
    ndx++;
    cx[ndx] = 1, cy[ndx] = 0;
    tau_top[ndx] = 5;
    tau_fluid[ndx] = 12;
    multiplier[ndx] = 0.01;
    ndx++;
    // phase of hex grid shifts these two entities
    // up
    cx[ndx] = 0;
    cy[ndx] = 1;
    tau_top[ndx] = 5;
    tau_fluid[ndx] = 12;
    multiplier[ndx] = 0.01;
    ndx++;
    cx[ndx] = 1;
    cy[ndx] = 1;
    tau_top[ndx] = 5;
    tau_fluid[ndx] = 12;
    multiplier[ndx] = 0.01;
    ndx++;
    // down
    cx[ndx] = 0;
    cy[ndx] = -1;
    tau_top[ndx] = 5;
    tau_fluid[ndx] = 12;
    multiplier[ndx] = 0.01;
    ndx++;
    cx[ndx] = 1;
    cy[ndx] = -1;
    tau_top[ndx] = 5;
    tau_fluid[ndx] = 11;
    multiplier[ndx] = 0.01;
    ndx++;
}

// same spec currently 
void CrossTalkSpecification::SetAggressiveHexGrid()
{
    hex_packed = true;
    Allocate(6);
    int ndx = 0;
    // left/right
    cx[ndx] = -1;
    cy[ndx] = 0;
    tau_top[ndx] = 5;
    tau_fluid[ndx] = 15;
    multiplier[ndx] = 0.01;
    ndx++;
    cx[ndx] = 1, cy[ndx] = 0;
    tau_top[ndx] = 5;
    tau_fluid[ndx] = 12;
    multiplier[ndx] = 0.01;
    ndx++;
    // phase of hex grid shifts these two entities
    // up
    cx[ndx] = 0;
    cy[ndx] = 1;
    tau_top[ndx] = 5;
    tau_fluid[ndx] = 12;
    multiplier[ndx] = 0.01;
    ndx++;
    cx[ndx] = 1;
    cy[ndx] = 1;
    tau_top[ndx] = 5;
    tau_fluid[ndx] = 12;
    multiplier[ndx] = 0.01;
    ndx++;
    // down
    cx[ndx] = 0;
    cy[ndx] = -1;
    tau_top[ndx] = 5;
    tau_fluid[ndx] = 12;
    multiplier[ndx] = 0.01;
    ndx++;
    cx[ndx] = 1;
    cy[ndx] = -1;
    tau_top[ndx] = 5;
    tau_fluid[ndx] = 11;
    multiplier[ndx] = 0.01;
    ndx++;
}

// hypothetically, claw back some of the intensity due to the buffering of the neighbors
// whether or not they supplied hydrogen ions
// but this is of course written wrongly to multiply by the number of neighbors
// but this is the way v7 rolls
float CrossTalkSpecification::ClawBackBuffering(int nei_total)
{
    // Rescale by the number of neighbors included in the calculation
    // to account for possible buffering of neighbors
    // but this happens in the wrong direction, so who knows what it is really doing?
    float scale = 1.0;
    if (nei_total>0)
        scale = nscale/nei_total;

    return 1.0/(cbulk*scale);
}

#define MAX_LINE_LEN    512
void CrossTalkSpecification::ReadCrossTalkFromFile(char *fname)
{
    struct stat fstatus;
    int         status;
    FILE *param_file;
    char *line;
    int nChar = MAX_LINE_LEN;

    int hex_tmp;
    int ndx = 0;
    int num_neighbor=0;
    int ax, ay;
    float tA,tB,tM;

    line = new char[MAX_LINE_LEN];

    status = stat(fname,&fstatus);

    if (status == 0)
    {
        // file exists
        printf("XTALK: loading parameters from %s\n",fname);

        param_file=fopen(fname,"rt");

        bool done = false;

        while (!done)
        {
            int bytes_read = getline(&line,(size_t *)&nChar,param_file);

            line[bytes_read]='\0';
            if (bytes_read > 0)
            {
                if (strncmp("hex_packed",line,10)==0)
                {
                    sscanf(line,"hex_packed: %d", &hex_tmp);
                    if (hex_tmp>0)
                        hex_packed = true;
                    else
                        hex_packed= false;
                    printf("hex_packed: %d\n", hex_tmp);
                }
                if (strncmp("num_neighbor",line,12)==0)
                {
                    sscanf(line, "num_neighbor: %d", &num_neighbor);
                    Allocate(num_neighbor);
                    ndx = 0;
                    printf("num_neighbor: %d\n",num_neighbor);
                }
                if (strncmp("a_neighbor",line,10)==0)
                {
                    sscanf(line,"a_neighbor: %d %d %f %f %f", &ax, &ay, &tA, &tB, &tM);
                    printf("a_neighbor: %d %d %f %f %f\n",ax, ay,tA,tB,tM);
                    cx[ndx] = ax;
                    cy[ndx] = ay;
                    tau_top[ndx] = tA;
                    tau_fluid[ndx] = tB;
                    multiplier[ndx] = tM;
                    ndx++;
                }
            }
            else
                done = true;
        }

        fclose(param_file);

    }
    else
        printf("XTALK: parameter file %s does not exist\n",fname);

    delete [] line;
}

void CrossTalkSpecification::NeighborByGridPhase(int &ncx, int &ncy, int cx, int cy, int cxd, int cyd, int phase)
{
    if (phase==0)
    {
        ncx = cx+cxd;
        ncy = cy+cyd;
    } else
    {
        ncy = cy+cyd;
        if (cyd!=0)
            ncx = cx+cxd-phase; // up/down levels are offset alternately on rows
        else
            ncx = cx+cxd;
    }
    // unless we're in a hex grid and need to know our offset before deciding
    // however those variables need to be passed
}


void CrossTalkSpecification::BootUpXtalkSpec(bool can_do_xtalk_correction, char *chipType, char *xtalk_name)
{
    if (can_do_xtalk_correction)
    {
        if (strlen(xtalk_name)>0)
        {
            ReadCrossTalkFromFile(xtalk_name);
        } else {
            if (strcmp (chipType, "318") == 0)
                SetNewHexGrid(); // find out who we really are!
            else if (strcmp(chipType,"900")==0)
                SetAggressiveHexGrid(); // 900 may have different cross-talk!
            else
                SetNewQuadGrid();
        }
    }
}
