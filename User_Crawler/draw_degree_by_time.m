function draw_degree_by_time()
    date_list = {'20120901', '20121001', '20121101', '20121201', '20130101', '20130201', '20130301', '20130401', '20130501', '20130601', '20130701', '20130801', '20130901', '20131001', '20131101', '20131201', '20140101', '20140201', '20140301', '20140401', '20140501', '20140601', '20140701', '20140801', '20140901', '20141001', '20141101', '20141201', '20150101', '20150201', '20150301', '20150401', '20150501', '20150601', '20150701', '20150801', '20150901', '20151001', '20151101', '20151201', '20160101', '20160201', '20160301', '20160401', '20160501', '20160601', '20160701', '20160801'};
    in_degree = [];
    out_degree = [];
    balance = [];
    reciprocity = [];
    balanced_p = [];
    for k=1:length(date_list)
        date = date_list{k};
        filepath = strcat('./data/graph/degree_', date, '.csv');
        dataset = csvread(filepath, 1, 1);
        in_degree = [in_degree mean(dataset(:,1))];
        out_degree = [out_degree mean(dataset(:,2))];
        temp = dataset(:,3);
        balance = [balance mean(temp(iswithin(temp, 0.0001, 10000)))];
        reciprocity = [reciprocity mean(dataset(:,4))];
        balanced_p = [balanced_p nnz(dataset(:,3) >= 0.5 & dataset(:,3) <= 2)/length(dataset(:,3))];
    end
    figure(1);
    dt = datenum(date_list, 'yyyymmdd');
    scatter(dt, in_degree, '*', 'MarkerEdgeColor', 'k');
    xlim([datenum('08-01-2012') datenum('08-01-2016')]);
    NumTicks = 5;
    L = get(gca,'XLim');
    set(gca,'XTick',linspace(L(1),L(2),NumTicks))
    datetick('x', 'mmm yyyy', 'keeplimits', 'keepticks');
    set(gca, 'FontSize', 12);
    xlabel(' ','FontSize',20);
    ax = gca;
    ax.XAxis.FontSize = 18;
    ylabel('Average In-degree','FontSize',20);
    title('');
    grid off;
    box on;
    print('./results/graph/in_degree_time.eps', '-depsc');
    
    figure(2);
    dt = datenum(date_list, 'yyyymmdd');
    scatter(dt, out_degree, '*', 'MarkerEdgeColor', 'k');
    xlim([datenum('08-01-2012') datenum('08-01-2016')]);
    NumTicks = 5;
    L = get(gca,'XLim');
    set(gca,'XTick',linspace(L(1),L(2),NumTicks))
    datetick('x', 'mmm yyyy', 'keeplimits', 'keepticks');
    set(gca, 'FontSize', 12);
    xlabel(' ','FontSize',20);
    ax = gca;
    ax.XAxis.FontSize = 18;
    ylabel('Average Out-degree','FontSize',20);
    title('');
    grid off;
    box on;
    print('./results/graph/out_degree_time.eps', '-depsc');
    
    figure(3);
    dt = datenum(date_list, 'yyyymmdd');
    scatter(dt, balance, '*', 'MarkerEdgeColor', 'k');
    xlim([datenum('08-01-2012') datenum('08-01-2016')]);
    NumTicks = 5;
    L = get(gca,'XLim');
    set(gca,'XTick',linspace(L(1),L(2),NumTicks))
    datetick('x', 'mmm yyyy', 'keeplimits', 'keepticks');
    set(gca, 'FontSize', 12);
    xlabel(' ','FontSize',20);
    ax = gca;
    ax.XAxis.FontSize = 18;
    ylabel('Average Balance','FontSize',20);
    title('');
    grid off;
    box on;
    print('./results/graph/balance_time.eps', '-depsc');
    
    figure(4);
    dt = datenum(date_list, 'yyyymmdd');
    scatter(dt, reciprocity, '*', 'MarkerEdgeColor', 'k');
    xlim([datenum('08-01-2012') datenum('08-01-2016')]);
    NumTicks = 5;
    L = get(gca,'XLim');
    set(gca,'XTick',linspace(L(1),L(2),NumTicks))
    datetick('x', 'mmm yyyy', 'keeplimits', 'keepticks');
    set(gca, 'FontSize', 12);
    xlabel(' ','FontSize',20);
    ax = gca;
    ax.XAxis.FontSize = 18;
    ylabel('Average Reciprocity','FontSize',20);
    title('');
    grid off;
    box on;
    print('./results/graph/reciprocity_time.eps', '-depsc');
    
    figure(5);
    dt = datenum(date_list, 'yyyymmdd');
    scatter(dt, balanced_p, '*', 'MarkerEdgeColor', 'k');
    ylim([0 1]);
    xlim([datenum('08-01-2012') datenum('08-01-2016')]);
    NumTicks = 5;
    L = get(gca,'XLim');
    set(gca,'XTick',linspace(L(1),L(2),NumTicks))
    datetick('x', 'mmm yyyy', 'keeplimits', 'keepticks');
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel(' ','FontSize',20);
    ax = gca;
    ax.XAxis.FontSize = 18;
    ylabel('Percentage of Balanced Users(%)','FontSize',20);
    title('');
    grid off;
    box on;
    print('./results/graph/balanced_percentage_time.eps', '-depsc');
    
    figure(6);
    dt = datenum(date_list, 'yyyymmdd');
    scatter(dt, in_degree + out_degree, '*', 'MarkerEdgeColor', 'k');
    xlim([datenum('08-01-2012') datenum('08-01-2016')]);
    NumTicks = 5;
    L = get(gca,'XLim');
    set(gca,'XTick',linspace(L(1),L(2),NumTicks))
    datetick('x', 'mmm yyyy', 'keeplimits', 'keepticks');
    set(gca, 'FontSize', 12);
    ax = gca;
    ax.XAxis.FontSize = 18;
    xlabel(' ','FontSize',20);
    ylabel('Average Degree','FontSize',20);
    title('');
    grid off;
    box on;
    print('./results/graph/degree_time.eps', '-depsc');
end

function flg=iswithin(x,lo,hi)
    flg= (x>=lo) & (x<=hi);
end
