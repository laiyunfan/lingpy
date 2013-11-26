# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2013-10-08 11:38
# modified : 2013-11-24 15:36
"""
Basic functions for the conversion of Python-internal data into strings.
"""

__author__="Johann-Mattis List"
__date__="2013-11-24"

import codecs
from ..settings import rcParams

try:
    import regex as re
except ImportError:
    import re
    print(rcParams['W_missing_module'].format('regex'))


def scorer2str(
        scorer
        ):
    """
    Convert a scoring function to a string.
    """
    
    # get sorted representation of characters
    chars = sorted(
            scorer.chars2int
            )

    # get the matrix
    matrix = scorer.matrix
    
    out = ''

    # write stuff to string
    for i,charA in enumerate(chars):
        out += charA
        for j,charB in enumerate(chars):
            out += '\t{0:.2f}'.format(scorer[charA,charB])
        out += '\n'

    return out

def msa2str(msa, wordlist=False, comment="#",
        _arange='{stamp}{comment}\n{meta}{comment}\n{body}'):
    """
    Function converts an MSA object into a string.
    """

    if 'stamp' in msa:
        stamp = msa['stamp']
    elif hasattr('stamp', msa):
        stamp = msa.stamp
    else:
        stamp = ''

    body = ''

    # if wordlist ist set to True, don't write the header line and put the
    # after comment
    if wordlist:

        formatter = max([len(t) for t in msa['taxa']])
        #body += '# ' +msa['seq_id']+'\n'
        for a,b,c in zip(msa['ID'],msa['taxa'],msa['alignment']):
            body += '{0}\t{1}'.format(a, b.ljust(formatter,'.'))+'\t'
            body += '\t'.join(c)+'\n'
        alm_len = len(c)

    elif type(msa) == dict:
        # get formatter
        formatter = max([len(t) for t in msa['taxa']])
        body += msa['dataset']+'\n'
        body += msa['seq_id']+'\n'
        for a,b in zip(msa['taxa'],msa['alignment']):
            body += a.ljust(formatter,'.')+'\t'
            body += '\t'.join(b)+'\n'
        alm_len = len(b)
    else:
        # get formatter
        formatter = max([len(t) for t in msa.taxa])
        body += msa.dataset+'\n'
        body += msa.seq_id+'\n'
        for a,b in zip(msa.taxa,msa.alm_matrix):
            body += a.ljust(formatter,'.')+'\t'
            body += '\t'.join(b)+'\n'
        alm_len = len(b)
    
    if 'local' in msa:
        local = msa['local']
    elif hasattr(msa,'local'):
        local = msa.local
    else:
        local = False

    if 'swaps' in msa:
        swaps = msa['swaps']
    elif hasattr(msa,'swaps'):
        swaps = msa.swaps
    else:
        swaps = False

    if 'consensus' in msa:
        consensus = msa['consensus']
    elif hasattr(msa, 'consensus'):
        consensus = msa.consensus
    else:
        consensus = False
    

    meta = ''

    if wordlist:
        meta += '0\t'+'COLUMNID'.ljust(formatter,'.')+'\t'+'\t'.join([str(i+1) for i in range(len(msa['alignment'][0]))])
        meta += '\n#\n'

    if local:
        if wordlist:
            meta += '{0}\t{1}\t'.format(0,'LOCAL'.ljust(formatter, '.'))
        else:
            meta += '{0}\t'.format('LOCAL'.ljust(formatter, '.'))
        tmp = []
        for i in range(alm_len):
            if i in local:
                tmp += ['*']
            else:
                tmp += ['.']
        meta += '\t'.join(tmp)+'\n'
    if swaps:
        if wordlist:
            meta += '{0}\t{1}\t'.format(0,'CROSSED'.ljust(formatter, '.'))
        else:
            meta += '{0}\t'.format('SWAPS'.ljust(formatter, '.'))
        tmp = alm_len * ['.']
        for swap in swaps:
            a,b,c = swap
            tmp[a] = '+'
            tmp[b] = '-'
            tmp[c] = '+'
        meta += '\t'.join(tmp)+'\n'

    if consensus:
        if wordlist:
            meta += '{0}\t{1}\t'.format(0,'CONSENSUS'.ljust(formatter, '.'))
        else:
            meta += '{0}\t'.format('CONSE'.ljust(formatter, '.'))
        meta += '\t'.join(consensus)+'\n'

    return _arange.format(
            stamp=stamp,
            meta=meta,
            body=body,
            comment=comment
            )

def matrix2dst(
        matrix,
        taxa = None,
        stamp = '',
        filename = '',
     ):
    """
    Convert matrix to dst-format.
    """
    if not taxa:
        taxa = ['t_{0}'.format(i) for i in range(len(matrix))]

    out = ' {0}\n'.format(len(taxa))
    for i,taxon in enumerate(taxa):
        out += '{0:10}'.format(taxon)[0:11]
        out += ' '.join(['{0:2f}'.format(d) for d in
            matrix[i]])
        out += '\n'
    if stamp:
        out += '# {0}'.format(stamp)
    if not filename:
        return out
    else:
        f = codecs.open(filename+'.dst','w','utf-8')
        f.write(out)
        f.close()
        if rcParams['verbose']: print(rcParams['fw'].format('dst')) # (filename,'dst'))

def pap2nex(
        taxa,
        paps,
        missing=0,
        filename=''
        ):
    """
    Function converts a list of paps into nexus file format.

    """
    out = '#NEXUS\n\nBEGIN DATA;\nDIMENSIONS ntax={0} NCHAR={1};\n'
    out += "FORMAT DATATYPE=STANDARD GAP=- MISSING={2} interleave=yes;\n"
    out += "MATRIX\n\n{3}\n;\n\nEND;"
    
    # get longest taxon
    maxTax = max([len(taxon) for taxon in taxa])

    # check whether paps are dict or list
    try:
        paps.keys()
        new_paps = []
        for key in paps:
            new_paps.append(paps[key])
    except:
        new_paps = paps

    # create the matrix
    matrix = ""
    
    for i,taxon in enumerate(taxa):
        tmp = '{0:XXX} '
        matrix += tmp.replace('XXX',str(maxTax)).format(taxon)
        matrix += ''.join([str(line[i]) for line in new_paps])
        matrix += '\n'
    
    if not filename:
        return out.format(
                len(taxa),
                len(paps),
                missing,
                matrix
                )
    else:
        f = codecs.open(filename+'.nex','w')
        f.write(
                out.format(
                    len(taxa),
                    len(paps),
                    missing,
                    matrix
                    )
                )
        f.close()
        
        if rcParams['verbose']: print(rcParams['M_file_written'].format(filename+'.nex'))
        return

def pap2csv(
        taxa,
        paps,
        filename=''
        ):
    """
    Write paps created by the Wordlist class to a csv-file.
    """

    out = "ID\t"+'\t'.join(taxa)+'\n'
    for key in sorted(paps,key=lambda x: int(re.sub(r'[^0-9]+','',str(x)))):
        out += '{0}\t{1}\n'.format(
            key,
            '\t'.join(str(i) for i in paps[key])
            )
    
    if not filename:
        return out
    else:
        f = codecs.open(filename+'.csv','w',"utf-8")
        f.write(out)
        f.close()

        if rcParams['verbose']: print(rcParams['M_file_written'].format(filename+'.csv'))
        
        return
