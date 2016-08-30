# cd('E:\\SHARED\\DEV\\KICAD\\_PROJECTS\\_utils\\LABEL_BUSTINE')
# execfile('create_labels.py')

resistor_values = [1,	7.5,	10,		22,		39,		47,		68,		75,		100,	130,	150,	220,	360,	470,	680,	1];
resistor_units  = ['','',	'',	'', '',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',		'k'];

resistor_values.extend([1.3,	1.8,	2.2,	3,		3.6,	3.9,	4.7,	5.6,	6.8,	8.2,	10,		12,		22,		33,		39,		47]);
resistor_units.extend( ['k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'k']);

resistor_values.extend([56,		68,		100, 	130,	150,	180,	220,	270,	330,	390,	470,	560,	680,	1,		2.7,	3.3]);
resistor_units.extend( ['k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'k',	'M',	'M',	'M']);

resistor_values.extend([4.7,	10]);
resistor_units.extend( ['M',	'M']);

rows_per_page = 4;
cols_per_page = 5;
row_spacing = 45000000;
col_spacing = 55000000;

create_grid = True;
create_labels = True;

brd = pcbnew.GetBoard();
ref_layer_name = 'REF';

# collect all tracks in reference layer 
ref_trks = [];
trks = list(brd.GetTracks());
for trk in trks:
	if trk.GetLayerName() == ref_layer_name:
		ref_trks.append(trk);

# collect all drawings in reference layer 
ref_dwgs = [];
dwgs = list(brd.GetDrawings());
for dwg in dwgs:
	if dwg.GetLayerName() == ref_layer_name:
		ref_dwgs.append(dwg);
		
# merge the lists
ref_objs = [];
for obj in ref_trks:
	ref_objs.append(obj);
for obj in ref_dwgs:
	ref_objs.append(obj);

# calculate bounding box
xmin = ymin = 2000000000;
xmax = ymax = 0;
for obj in ref_objs:
	bb = obj.GetBoundingBox();
	xmin = min(xmin, bb.GetX());
	xmax = max(xmax, bb.GetRight());
	ymin = min(ymin, bb.GetY());
	ymax = max(ymax, bb.GetBottom());
	
row_offset =  ymin;
col_offset =  xmin;
	
# plot grid on DRAWINGS layer
if create_grid:
	dwg_user_layer = 40;
	assert(brd.GetLayerName(dwg_user_layer) == 'Dwgs.User')
	x = col_offset;
	for col_count in range(0, (cols_per_page+1)):
		# print col_count, y
		vline = pcbnew.DRAWSEGMENT(brd);
		vline.SetLayer(dwg_user_layer);
		vline.SetStart(pcbnew.wxPoint(x, row_offset));
		vline.SetEnd(pcbnew.wxPoint(x, row_offset + row_spacing*rows_per_page));	
		brd.Add(vline);
		x = x + col_spacing;
	y = row_offset;
	for row_count in range(0, (rows_per_page+1)):
		# print row_count, y
		hline = pcbnew.DRAWSEGMENT(brd);
		hline.SetLayer(dwg_user_layer);
		hline.SetStart(pcbnew.wxPoint(col_offset, y));
		hline.SetEnd(pcbnew.wxPoint(col_offset + col_spacing*cols_per_page, y));	
		brd.Add(hline);
		y = y + row_spacing;
	
# copy objects
if create_labels:
	curr_page = 0;
	curr_col = 0;
	curr_row = 0;
	for idx in range(0, len(resistor_values)):
		val = resistor_values[idx];
		unit = resistor_units[idx];	
		
		# select layer corresponding to current page
		layer_name = "P%d" % curr_page;	
		layer_found = False;
		for layer_idx in range(0, brd.GetCopperLayerCount()):
			if brd.GetLayerName(layer_idx) == layer_name:
				layer_found = True;
				break;	
		assert(layer_found);
		
		# translation
		dx = curr_col * col_spacing;
		dy = curr_row * row_spacing;
		
		for obj in ref_objs:
			if obj.__class__ == pcbnew.TEXTE_PCB:
				obj_new = pcbnew.TEXTE_PCB(obj);
				obj_new.Copy(obj);
				value_str = "%0.1f" % resistor_values[idx];
				unit_str = resistor_units[idx];
				
				if obj.GetText() == '_v0':
					obj_new.SetText(value_str);
				elif obj.GetText() == '_v1':
					obj_new.SetText(value_str);
				elif obj.GetText() == '_u0':
					obj_new.SetText(unit_str);
				elif obj.GetText() == '_u1':
					obj_new.SetText(unit_str);	
				else:
					obj_new.SetText(obj.GetText());	
				center = obj.GetPosition();			
				obj_new.SetPosition(pcbnew.wxPoint(center.x + dx, center.y + dy));
				obj_new.SetSize(obj.GetSize());
					
			elif obj.__class__ == pcbnew.TRACK:
				obj_new = pcbnew.TRACK(obj);
				p1 = obj.GetStart();
				p2 = obj.GetEnd();
				start = pcbnew.wxPoint(p1.x + dx, p1.y + dy);
				end = pcbnew.wxPoint(p2.x + dx, p2.y + dy);
				obj_new.SetStart(start);
				obj_new.SetEnd(end);
				
			else:
				assert(False);			
			obj_new.SetLayer(layer_idx);
			
			# add new object to layer
			brd.Add(obj_new);
		
		curr_col = curr_col + 1;
		if curr_col >= cols_per_page:
			curr_col = 0;
			curr_row = curr_row + 1;
			if curr_row >= rows_per_page:
				curr_row = 0;
				curr_page = curr_page + 1;
		
		


	
	
	
	