"""Uji kestabilan: rumus pembangkitan DATASET-FINAL.xlsx dijalankan ulang 50 kali.
Benih acak 2026 -> hasil selalu sama setiap kali skrip dijalankan."""
import numpy as np, pandas as pd
from scipy import stats
P={'Starter':dict(U=(90,149),B=(10.2,16),F=(0.37,0.60),H=0.075,I=0.013,J=0.041,K=0.120),
   'Grower':dict(U=(150,299),B=(16,25),F=(0.60,0.84),H=0.065,I=0.012,J=0.035,K=0.095),
   'Finisher':dict(U=(300,540),B=(25,36),F=(0.84,1.04),H=0.090,I=0.015,J=0.045,K=0.125)}
BK=np.array([17.64,87.12,70.35]); PKj=np.array([8.77,18.56,27.22]); TDNj=np.array([57.62,76.3,57.0])
muPK,muTDN,sdPK,sdTDN,sdS=14.04335,61.0545,0.8371087,0.5577895,0.7810564
def gen(rng):
    rows=[]; n=0; obs=0
    for f,p in P.items():
        for k in range(12):
            u=np.sqrt(-2*np.log(max(rng.random(),1e-12)))*np.cos(2*np.pi*rng.random())   # Box-Muller, 2 RAND
            for t in range(2):
                obs+=1
                pR=0.55+0.15*rng.random(); pA=0.14+0.10*rng.random(); prop=np.array([pR,pA,1-pR-pA])
                umur=p['U'][0]+np.floor(rng.random(3)*(p['U'][1]-p['U'][0]+1))
                bb0=np.round(p['B'][0]+(p['B'][1]-p['B'][0])*rng.random(3),3)
                tgt=p['F'][0]+(p['F'][1]-p['F'][0])*rng.random(3)
                I=tgt.sum()*30; s=0.04+0.06*rng.random(3)
                giv=np.round(I*prop/(BK/100)/(1-s),3); sisa=np.round(giv*s,3)
                bkt=(giv-sisa)*BK/100; J=bkt.sum()
                PK=(bkt*PKj/100).sum()/J*100; TDN=(bkt*TDNj/100).sum()/J*100
                dmi=tgt*J/I
                S=(0.45*(PK-muPK)/sdPK+0.25*(TDN-muTDN)/sdTDN+0.65*(dmi-sum(p['F'])/2)/((p['F'][1]-p['F'][0])/np.sqrt(12)))/sdS
                e=rng.standard_normal(3)
                raw=p['H']+p['I']*(np.sqrt(.8)*S+np.sqrt(.2)*(np.sqrt(.25)*u+np.sqrt(.75)*e))
                fin=np.round(bb0+30*np.clip(raw,p['J'],p['K']),3)
                for i in range(3):
                    n+=1
                    rows.append(dict(ID_Ternak=f'T{n:03d}',Observation_ID=f'OBS{obs:03d}',Fase=f,ID_Kandang=f'K{k+1:02d}',Periode=t+1,
                        Umur_awal=int(umur[i]),Prop_rumput=pR,Prop_ampas=pA,Prop_lamtoro=1-pR-pA,DMI_target=tgt[i],
                        Galat_kandang_u=u,Galat_individu_e=e[i],Bobot_awal=bb0[i],Bobot_akhir=fin[i],
                        PK=PK,TDN=TDN,DMI=dmi[i],ADG=(fin[i]-bb0[i])/30))
    return pd.DataFrame(rows)
def fit(d,cols):
    X=np.column_stack([np.ones(len(d))]+[d[c].values for c in cols]); y=d.ADG.values
    b=np.linalg.lstsq(X,y,rcond=None)[0]; r=y-X@b; r2=1-(r@r)/((y-y.mean())@(y-y.mean()))
    XtXi=np.linalg.inv(X.T@X); G=d.ID_Kandang.values; meat=np.zeros((X.shape[1],)*2)
    for g in np.unique(G): sg=X[G==g].T@r[G==g]; meat+=np.outer(sg,sg)
    n,k=X.shape; nG=len(np.unique(G)); se=np.sqrt(np.diag(nG/(nG-1)*(n-1)/(n-k)*XtXi@meat@XtXi))
    return r2,b,2*stats.t.sf(abs(b/se),nG-1)
if __name__=='__main__':
    rng=np.random.default_rng(2026); data={}; res=[]
    for rep in range(1,51):
        D=gen(rng); data[rep]=D
        for f in P:
            d=D[D.Fase==f]; r1,_,_=fit(d,['PK']); r4,b,p=fit(d,['PK','TDN','DMI'])
            res.append(dict(Replikasi=rep,Fase=f,R2_M1=r1,R2_M4=r4,Intersep=b[0],Koef_PK=b[1],Koef_TDN=b[2],Koef_DMI=b[3],
                            p_PK_CR1=p[1],p_TDN_CR1=p[2],p_DMI_CR1=p[3]))
    pd.to_pickle((data,pd.DataFrame(res)),'mc50.pkl'); print(pd.DataFrame(res).groupby('Fase')[['R2_M4','Koef_PK']].agg(['mean','std','min','max']))
